import React, { Component } from 'react'
import {API} from './backend'

class SignupOnBoard extends Component {

    constructor(props){
        super(props)
        this.state = {
            token: '',
            regno: '',
            password1: '',
            password2: '',
            mobile: '',
            branch: '',
            photo: null,
            error: '',
            isVerified: true   //displaying error on fake user
        }
    }

    componentDidMount(){
        const { match: { params } } = this.props;
        fetch(`${API}/verify/${params.uid}/${params.token}`, {
            method: 'GET'
        })
        .then(response => {
            return response.json()
        })
        .then(data => {
            console.log(data)
            this.setState({mobile: data.student.mob, branch: data.student.branch, regno: data.student.user, token: data.token})
        })
    }

    handleClick = event => {
        event.preventDefault();
        if(this.state.password1 !== this.state.password2){
            this.setState({error: "Passwords Don't Match!!"})
        }else{
            console.log(this.state)
            let form_data = new FormData();
            form_data.append('profile_pic', this.state.photo, this.state.photo.name);

            fetch(`${API}/onboard`, form_data, {
                method: 'POST',
                headers: {
                    'Content-Type': 'multipart/form-data',
                    'Authorization': `Token ${this.state.token}`,
                    'mob': this.state.mobile,
                    'password': this.state.password1,
                    'password2': this.state.password2,
                    'regno': this.state.regno
                }
            })
            .then(response => {
                if(response.status === 200){
                return response.json()
                }else{
                    console.log(response)
                }
            })
            .then(data => {
                console.log(data)
            })
        }
    }

    handleChange = name => event => {
        this.setState({error: ''})
        this.setState({
            [name]: event.target.value
        })
    }

    handleImageChange = (e) =>{
        this.setState({
            photo: e.target.files[0]
          })
    }

    render(){
        return(
            <div>
            <div className='login-grid-container'>
                <div className='login-grid-item1'>
                    <h1 style={{fontSize:'4.2rem'}}>GETTING <br /> YOU ONBOARD</h1>
                    <div className='login-doodles'>
                        <img style={{width:'23em', float:'left'}} src='/images/onBoard.svg' alt='doodle' />
                    </div>
                </div>
                <div className='login-grid-item2' style={{marginBottom: '2em'}}>
                    <div className='login-form'>
                        <p className='email-verify'>EMAIL VERIFIED SUCCESSFULLY</p>
                        <form>

                            {this.state.error}

                            <input className='field-input' style={{margin:'0.3em 0'}} value={this.state.password1} onChange={this.handleChange('password1')}  type='password' placeholder='Enter Password' /><br/>
                            <input className='field-input' style={{margin:'0.3em 0'}} value={this.state.password2} onChange={this.handleChange('password2')} type='password' placeholder='Confirm Password' /><br/>
                            <input className='field-input' style={{margin:'0.3em 0'}} value={this.state.mobile} onChange={this.handleChange('mobile')} type='text' placeholder='Mobile No.' /><br/>
                            <input className='field-input' style={{margin:'0.3em 0'}} value={this.state.branch} onChange={this.handleChange('branch')} type='text' placeholder='Branch' /><br/>
                            <input style={{fontSize: '1rem', marginBottom: '1em'}} onChange={this.handleImageChange} type='file' accept="image/png, image/jpeg" required />
                            <div className='btn-outline'><button onClick={this.handleClick} className='login-btn'>CREATE ACCOUNT</button></div>

                            <p>{this.state.token}</p>
                        </form>
                        <h2><a href='/login'>LOGIN </a>HERE</h2>
                    </div>
                </div>
            </div>
            </div>
        )
    }
}

export default SignupOnBoard;