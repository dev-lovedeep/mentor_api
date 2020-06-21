import React, { Component } from 'react'
import {API} from './backend'
import {createAcc} from './apicalls'

class SignupOnBoard extends Component {

    constructor(props){
        super(props)
        this.state = {
            password1: '',
            password2: '',
            mobile: '',
            branch: '',
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
            this.setState({mobile: data.student.mob, branch: data.student.branch})
        })
    }

    handleClick = event => {
        event.preventDefault();
        if(this.state.password1 !== this.state.password2){
            this.setState({error: "Passwords Don't Match!!"})
        }else{
            createAcc([this.state.mobile, this.state.password1, this.state.password2,])
        }
    }

    handleChange = name => event => {
        this.setState({error: ''})
        this.setState({
            [name]: event.target.value
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
                            <input style={{fontSize: '1rem', marginBottom: '1em'}} type='file' placeholder='Select Image' />
                            <div style={{marginBottom:'2em', color:'#FF8585', fontWeight: '600'}}><input style={{width:'1.2em', height: '1.2em', position:'relative', left:'-0.5em'}} type='checkbox' name='termsNconditions' /><label for='termsNconditions'>I Have Read All Terms & Conditions</label></div>
                            <div className='btn-outline'><button onClick={this.handleClick} className='login-btn'>CREATE ACCOUNT</button></div>
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