import React from 'react'

export default function ToggleButton({toggler, toggleState}) {
    function handleClick(evt){
        evt.preventDefault()
        toggler()
      }
    return (
    
    <>
        <div className=''>
            <div>
                {toggleState < 0 ? 'Already registered?' : 'New User?'}<span> </span>
                </div>
                <div>
                <button
                    className="text-land"
                    onClick={handleClick}
                >{toggleState < 0 ? 'Log in' : 'Sign up'}</button>
            </div>
        </div>
    </>

  )
}
