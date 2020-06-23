import React, { Component } from 'react'
import {API} from './backend'
import Header from './header'
import { Redirect } from 'react-router-dom';

class SignupOnBoard extends Component {

    constructor(props){
        super(props)
        this.state = {
            uid: '',
            email_token: '',
            token: '',
            regno: '',
            password1: '',
            password2: '',
            mobile: '',
            branch: '',
            photo: null,
            error: '',
            isVerified: true,   //displaying error on fake user
            performRedirect: false
        }
    }

    componentDidMount(){
        const { match: { params } } = this.props;
        this.setState({uid: params.uid, email_token: params.token})
        fetch(`${API}/verify/${params.uid}/${params.token}`, {
            method: 'GET'
        })
        .then(response => {
            return response.json()
        })
        .then(data => {
            if(data.success === 'false'){
                this.setState({isVerified: false})
            }else{
                this.setState({mobile: data.student.mob, branch: data.student.branch, regno: data.student.user, token: data.token})  
            }
        })
    }

    handleClick = event => {
        event.preventDefault();
        if(this.state.password1 !== this.state.password2){
            this.setState({error: "Passwords Don't Match!!"})
        }else{
            console.log(this.state)
            let form_data = new FormData();
            form_data.append('profile_pic', this.state.photo);
            form_data.append('mob', this.state.mobile);
            form_data.append('password', this.state.password1);
            form_data.append('password2', this.state.password2);
            form_data.append('regno', this.state.regno);
            form_data.append('uidb64', this.state.uid);
            form_data.append('email_token', this.state.email_token);

            fetch(`${API}/onboard/`, {
                method: 'POST',
                body: form_data
            })
            .then(response => {
                if(response.status === 200){
                this.setState({performRedirect: true})
                return response.json()
                }else{
                    this.setState({error: "An Error Has Occured, Try Again!!"})
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
            {this.state.performRedirect && 
            <Redirect to='/login' />}

            <Header role="1" />

            {this.state.isVerified && 
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

                        </form>
                        <h2><a href='/login'>LOGIN </a>HERE</h2>
                    </div>
                </div>
            </div>}


            {!this.state.isVerified && 
            <h1>Unauthorised Access!!</h1>}
            </div>
        )
    }
}

export default SignupOnBoard;