import React from 'react'
import { useState } from 'react'
import * as userService from '../../utilities/users-service'
import { Link } from 'react-router-dom'
const initialState = {
    username: '',
    email: '',
    password:'',
    password2:''

}

export default function LoginForm({ user, setuser }) {
    const [credentials, setCredentials] = useState(initialState);
    const [error, setError] = useState('');

    const disable = false;

    function handleChange(evt){
        setCredentials({...credentials, [evt.target.name]:evt.target.value})
    }

    // handlesubmit() -> invokes signUp() function 
    async function handleSubmit(evt){
        evt.preventDefault();
        console.log("submitted")
        try {
            console.log("handleSubmit")
            console.log(credentials)
            const newUser = await userService.signUp(credentials)
            console.log(newUser)
            setuser(newUser)
        } catch(error){
            setError('Signup Failed - Try Again');
        }

    }

    return (
        <>
            <div>SignUp</div>
            <div className="rounded-md m-5 bg-afterhour text-lining">
                <form autoComplete="off" onSubmit={handleSubmit}>
                    <div className='relative flex-row justify-between mt-2 mb-2'>
                        <label>username</label>
                        <input 
                            type="text" 
                            name="username" 
                            value={credentials.username}
                            onChange={handleChange}
                            required></input>
                    </div>
                    <div className='relative flex-row justify-between mt-2 mb-2'>
                        <label>email</label>
                        <input 
                            type="email" 
                            name="email" 
                            value={credentials.email}
                            onChange={handleChange}
                            required></input>
                    </div>
                    <div className='relative flex-row justify-between mt-2 mb-2'>
                        <label>password</label>
                        <input 
                            type="password" 
                            name="password" 
                            value={credentials.password}
                            onChange={handleChange}
                            required></input>
                    </div>
                    <div className='relative flex-row justify-between mt-2 mb-2'>
                        <label>confirm password</label>
                        <input 
                            type="password" 
                            name="password2" 
                            value={credentials.password2}
                            onChange={handleChange}
                            required></input>
                    </div>
                    <button className=' text-cardamom bg-vanilla hover:bg-land hover:text-vanilla py-1 px-1 rounded mt-5 mb-5' 
                        type="submit" 
                        
                        >SIGN UP</button>
                </form>

            </div>
        </>
    )
}
