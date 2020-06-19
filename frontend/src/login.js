import React, { Component } from 'react'

class Login extends Component {
    
    render(){
        return(
            <div className='login-grid-container'>
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
                            <input className='field-input' type='text' placeholder='Enter Registration No.' /><br/>
                            <input className='field-input' type='password' placeholder='Password' />
                            <div className='btn-outline'><button className='login-btn'>LOGIN</button></div>
                        </form>
                        <p style={{fontWeight:'600', marginBottom:'3em'}}>forgot password? <span><a href='#'>Click here!!</a></span></p>
                        <h2><a href='#'>SIGNUP </a>HERE</h2>
                    </div>
                </div>
            </div>
        )
    }
}

export default Login;