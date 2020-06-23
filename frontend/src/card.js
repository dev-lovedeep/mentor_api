import React from 'react'

function Card(props) {
    return  (
        <div style={{width: '100%', textTransform: 'capitalize'}}>
            <div className='grid-container-card'>
                <div className='card-img'>
                    <img src={props.imgUrl} alt="Img" />
                </div>
                <div className='card-details'>
                    <p><b>NAME: </b>{props.name}</p>
                    <p><b>REG. NO.: </b>{props.regno}</p>
                    <p><b>BRANCH: </b>{props.branch}</p>
                    <p><b>MOBILE: </b>{props.mobile}</p>
                </div>
            </div>
        </div>
    )
}

export default Card