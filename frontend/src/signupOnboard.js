import React, { Component } from 'react'

class SignupOnBoard extends Component {
    
    render(){
        return(
            <div className='login-grid-container'>
                <div className='login-grid-item1'>
                    <h1 style={{fontSize:'4.2rem'}}>GETTING <br /> YOU ONBOARD</h1>
                    <div className='login-doodles'>
                        <img style={{width:'23em', float:'left'}} src='/images/onBoard.svg' />
                    </div>
                </div>
                <div className='login-grid-item2' style={{marginBottom: '2em'}}>
                    <div className='login-form'>
                        <p className='email-verify'>EMAIL VERIFIED SUCCESSFULLY</p>
                        <form>
                            <input className='field-input' style={{margin:'0.3em 0'}} type='password' placeholder='Enter Password' /><br/>
                            <input className='field-input' style={{margin:'0.3em 0'}} type='password' placeholder='Confirm Password' /><br/>
                            <input className='field-input' style={{margin:'0.3em 0'}} type='text' placeholder='Mobile No.' /><br/>
                            <input className='field-input' style={{margin:'0.3em 0'}} type='text' placeholder='Branch' /><br/>
                            <input style={{fontSize: '1rem', marginBottom: '1em'}} type='file' placeholder='Select Image' />
                            <div style={{marginBottom:'2em', color:'#FF8585', fontWeight: '600'}}><input style={{width:'1.2em', height: '1.2em', position:'relative', left:'-0.5em'}} type='checkbox' name='termsNconditions' /><label for='termsNconditions'>I Have Read All Terms & Conditions</label></div>
                            <div className='btn-outline'><button className='login-btn'>CREATE ACCOUNT</button></div>
                        </form>
                        <h2><a href='#'>LOGIN </a>HERE</h2>
                    </div>
                </div>
            </div>
        )
    }
}

export default SignupOnBoard;