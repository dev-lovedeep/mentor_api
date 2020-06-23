import React from 'react'

function Header(props)  {
    
        return(
            <div className='app-header'>
                <span className='header-name'>
                <p style={{margin:'0'}}>FIND YOUR PAL</p>
                </span>
                <span className='login-state'>

                    {props.role === "1" &&
                    <p><a href='/login' style={{color: '#fff'}}>LOGIN</a></p>}

                    {props.role === "2" &&
                    <p><a href='/signup' style={{color: '#fff'}}>SIGNUP</a></p>}

                    {props.role === "3" &&
                    <p><img src={props.img_url} style={{height: '3.5rem', width: '3.5rem'}} alt='UserImg' />{props.username}</p>}
                </span>
            </div>
        )

}

export default Header