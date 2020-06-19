import React, { Component } from 'react'

class Header extends Component {
    
    render() {
        return(
            <div className='app-header'>
                <span className='header-name'>
                <p style={{margin:'0'}}>FIND YOUR PAL</p>
                </span>
                <span className='login-state'>
                    <p>STATE</p>
                </span>
            </div>
        )
    }
}

export default Header