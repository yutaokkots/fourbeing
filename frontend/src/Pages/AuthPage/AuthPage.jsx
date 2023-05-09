import React, { useState } from 'react'
import LoginForm from '../../components/Authcomponents/LoginForm'
import SignupForm from '../../components/Authcomponents/SignupForm'
import ToggleButton from '../../components/Authcomponents/ToggleButton'


export default function AuthPage( { user, setUser } ) {
    const [toggle, setToggle] = useState(1)

    // sets what is displayed on this page using unary, 
    // 1 for login, -1 for signup
    function handleToggle(){
        setToggle(-toggle)
    }

  return (
    <>
    <div>AuthPage</div>
    <div>
        {
            toggle > 0 ? (
                <>
                    <h1>-- loginform --</h1>
                <LoginForm user={ user } setUser={ setUser}/>
                </>
            )
                :
                (
                <>
                <h1>-- logoutform --</h1>
                <SignupForm user={ user } setUser={ setUser}/>
                </>
                )
        }
        <ToggleButton toggler={ handleToggle } toggleState={ toggle } />
        
    </div>
    </>
  )
}
