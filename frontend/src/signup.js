import React, { Component } from 'react'

class Signup extends Component {
    
    render(){
        return(
            <div className='login-grid-container' style={{marginBottom: '2em'}}>
                <div className='login-grid-item1'>
                    <h1 style={{fontSize:'4.2rem', marginLeft:'2em' ,marginBottom:'0.2em'}}>WELCOME <br /> TO MNNIT COMMUNITY</h1>
                    <div className='signup-doodles'>
                        <img style={{width:'30em', float:'left'}} src='/images/signup.png' />
                    </div>
                </div>
                <div className='login-grid-item2' style={{marginBottom: '2em'}}>
                    <div className='login-form'>
                        <h1>SIGNUP</h1>
                        <form>
                            <input type='text' placeholder='Enter Registration No.' /><br/>
                            <div className='btn-outline' style={{marginTop:'3em', marginBottom:'2em'}}><button className='login-btn'>SIGNUP</button></div>
                        </form>
                        <h2 style={{marginTop:'3em'}}><a href='#'>LOGIN </a>HERE</h2>
                    </div>
                </div>
            </div>
        )
    }
}

export default Signup;