import React, { Component } from 'react'
import {signup} from './apicalls'

class Signup extends Component {

    constructor(props){
        super(props)
        this.state = {
            regNo: '',
            error: '',
            success: ''
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
        signup(this.state.regNo)
        .then(data => {
            if(data.error){
                this.setState({error:data.error})
                console.log(data.error)
            }else{
                this.setState({success: data.success})
                console.log(data.success)
            }
        })
    }
    
    render(){
        return(
            <div className='login-grid-container' style={{marginBottom: '2em'}}>
                <div className='login-grid-item1'>
                    <h1 style={{fontSize:'4.2rem', marginLeft:'2em' ,marginBottom:'0.2em'}}>WELCOME <br /> TO MNNIT COMMUNITY</h1>
                    <div className='signup-doodles'>
                        <img style={{width:'30em', float:'left'}} src='/images/signup.png' alt='doodle' />
                    </div>
                </div>
                <div className='login-grid-item2' style={{marginBottom: '2em'}}>
                    <div className='login-form'>
                        <h1>SIGNUP</h1>
                        <form>
                            {this.state.error && 
                            <p>{this.state.error}</p>}
                            {this.state.success && 
                            <p>{this.state.success}</p>}
                            <input className='field-input' type='text' value={this.state.regNo} onChange={this.handleChange('regNo')} placeholder='Enter Registration No.' /><br/>
                            <div className='btn-outline' style={{marginTop:'3em', marginBottom:'2em'}}><button onClick={this.handleClick} className='login-btn'>SIGNUP</button></div>
                        </form>
                        <h2 style={{marginTop:'3em'}}><a href='/login'>LOGIN </a>HERE</h2>
                    </div>
                </div>
            </div>
        )
    }
}

export default Signup;