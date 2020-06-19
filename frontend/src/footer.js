import React, { Component } from 'react'

class Footer extends Component {
    
    render()
    {
        return(
            <div className='app-footer'>
                <p>Created By</p>
                <span><img className='heart' src='/images/heart.png' alt='Hearts' /></span>
                <p>Code_Pirates</p>
            </div>
        )
    }
}

export default Footer