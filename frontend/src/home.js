import React, { Component } from 'react'
import './home.css'
import Card from './card'
import { Redirect } from 'react-router-dom';
import {isAuthenticated} from './apicalls'
import Header from './header'
import { API } from './backend';

const token = JSON.parse(localStorage.getItem('jwt'))

class Home extends Component {

    constructor(props)
    {
        super(props);
        this.state = {
            query: '',
            branch: 'all',
            tag: 'all',
            name: '',
            img_src: '',
            isLoggedIn: true,
            search: null
        }

        this.handleChange = this.handleChange.bind(this)
        this.handleSubmit = this.handleSubmit.bind(this)
    }

    componentDidMount() {
        if(typeof window == 'undefined') {
            this.setState({isLoggedIn: false})
        }
        if(localStorage.getItem('jwt')) {
            this.setState({isLoggedIn: true})
            isAuthenticated()
            .then(data => {
                if(data.success === "false"){
                    if(typeof window !== 'undefined') {
                        localStorage.removeItem('jwt')
                        this.setState({isLoggedIn: false})
                    }
                }
                else if(data.success === "true"){
                    fetch(`${API}/detail/${data.user}`, {
                        method: 'GET',
                        headers: {
                            'Authorization': `Token ${token}`
                        }
                    })
                    .then(response => {
                        return response.json()
                    })
                    .then(data => {
                        this.setState({name: data.name, img_src: data.profile_pic})
                    })
                }
            })
        }
        else{
            this.setState({isLoggedIn: false})
        }

    }

    handleChange = name => event => {
        this.setState({
            [name]: event.target.value
        })
    }

    handleSubmit = event => {
        event.preventDefault();
        
        fetch(`${API}/filter/?query=${this.state.query}&branch=${this.state.branch}&tag=${this.state.tag}`, {
            method: 'GET',
            headers: {
                'Authorization': `Token ${token}`
            }
        })
        .then(response => {
            if(response.status === 200){
                return response.json()
            }
        })
        .then(data => {
            this.setState({search: data})
            console.log(this.state.search)
        })
    }

    render(){
        return(
            <div>
            <Header role="3" img_url={this.state.img_src} username={this.state.name} />
            <div className='home-grid-container'>
                {!this.state.isLoggedIn && 
                <Redirect to='/login' />}
                <div className='home-grid-item' style={{justifyContent: 'flex-end'}}>
                    <div className='pal-search-form'>
                        <form className='search-form'>
                            <label for='name'>Search By:</label>
                            <input type='text' className='field-input' 
                            placeholder='Name or Reg No.' 
                            name='name' 
                            value={this.state.query}
                            onChange={this.handleChange('query')} />
                            <label for='branch'>Branch:</label>
                            <select className='field-input'
                             name='branch' 
                             value={this.state.branch}
                             onChange={this.handleChange('branch')} >
                                <option value='all'>All</option>
                                <option value='cse'>CSE</option>
                                <option value='it'>IT</option>
                                <option value='ece'>ECE</option>
                                <option value='ee'>EE</option>
                                <option value='me'>ME</option>
                                <option value='ce'>CE</option>
                                <option value='cve'>Civil</option>
                                <option value='pie'>PIE</option>
                                <option value='bt'>BT</option>
                            </select>
                            <label for='branch'>Tags:</label>
                            <select className='field-input' 
                            name='tag' 
                            value={this.state.tag}
                            onChange={this.handleChange('tag')} >
                                <option value='all'>All</option>
                            </select>
                            <div className='btn-outline'>
                                <button className='login-btn' onClick={this.handleSubmit}>SEARCH</button>
                            </div>
                        </form>
                    </div>
                </div>
                <div className='home-grid-item'>
                    <div className='pal-search-list'>
                        {this.state.search &&
                        this.state.search.map((student, index) => (
                            <Card
                            imgUrl={student.profile_pic}
                            name={student.name} 
                            regno={student.user}
                            branch={student.branch}
                            mobile={student.mob}
                            />
                        ))
                        }
                    </div>
                </div>
            </div>
            </div>
        )
    }
}

export default Home;