import React, { Component } from 'react'
import {login} from './apicalls'
import Header from './header'
import {Redirect} from 'react-router-dom'

class Login extends Component {

    constructor(props){
        super(props)
        this.state = {
            regNo: '',
            password: '',
            performRedirect: false,
            error: ''
        }
    }

    componentDidMount() {
        if(typeof window == 'undefined') {
            this.setState({performRedirect: false})
        }
        if(localStorage.getItem('jwt')) {
            this.setState({performRedirect: true})
        }
        else{
            this.setState({performRedirect: false})
        }
    }

    handleChange = name => event => {
        this.setState({error: ''})
        this.setState({success: ''})
        this.setState({
            [name]: event.target.value
        })
    }

    handleClick = event => {
        event.preventDefault();
        login(this.state.regNo, this.state.password)
        .then(data => {
            if(data !== 'undefined' && data !== ''){
            if(typeof window !== 'undefined') {
                localStorage.setItem('jwt', JSON.stringify(data.token))
            }
            this.setState({performRedirect: true})
        } else{
            this.setState({error: "Username & Password Don't Match!!"})
        }
        })
        .catch(err => console.log(err))
    }
    
    render() {
        return(
            <div>
            <Header role="2" />
            <div className='login-grid-container'>
                {this.state.performRedirect &&
                <Redirect to='/home' />}
                <div className='login-grid-item1'>
                    <h1 style={{fontSize:'4.2rem', marginBottom:'0.2em'}}>FIND FROM <br /> STUDENTS OF MNNIT</h1>
                    <div className='login-doodles'>
                        <img style={{width:'16em'}} src='/images/Login1.svg' alt='Doodle' />
                        <img style={{position:'relative' , top:'2.5em'}} src='/images/Login2.svg'  alt='Doodle' />
                        <img src='/images/Login3.svg' alt='Doodle' />
                    </div>
                </div>
                <div className='login-grid-item2'>
                    <div className='login-form'>
                        <h1>LOGIN</h1>
                        <form>
                            {<p>{this.state.error}</p>}
                            <input className='field-input' value={this.state.regNo} onChange={this.handleChange('regNo')} type='text' placeholder='Enter Registration No.' /><br/>
                            <input className='field-input' value={this.state.password} onChange={this.handleChange('password')} type='password' placeholder='Password' />
                            <div className='btn-outline'><button onClick={this.handleClick} className='login-btn'>LOGIN</button></div>
                        </form>
                        <p style={{fontWeight:'600', marginBottom:'3em'}}>forgot password? <span><a href='#'>Click here!!</a></span></p>
                        <h2><a href='/signup'>SIGNUP </a>HERE</h2>
                    </div>
                </div>
            </div>
            </div>
        )}
}

export default Login;