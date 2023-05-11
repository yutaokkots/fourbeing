import React from 'react'
import { useState, useContext } from 'react'
import * as userService from '../../utilities/users-service'
import { Link, useNavigate  } from 'react-router-dom'
import { AuthContext } from "../../Pages/App"
import * as usersAPI from '../../utilities/users-api'

const initialState = {
    username: '',
    email: '',
    password:'',
    passwordConfirm:''

}

export default function LoginForm() {
    const [credentials, setCredentials] = useState(initialState);
    const navigate = useNavigate()
    const { user, setUser } = useContext(AuthContext)

    const [error, setError] = useState('');

    const disable = false;

    function handleChange(evt){
        setCredentials({...credentials, [evt.target.name]:evt.target.value})
    }
    // handlesubmit() -> invokes signUp() function 
    async function handleSubmit(evt){
        evt.preventDefault();
        console.log("submitted")
        await userService.signUp(credentials).then((response) => {
            console.log(response)
            
        }).then((response) => {
            setUser(response)
        }).catch((error) => {
            setError('Signup Failed - Try Again', error);
        })
        setUser(usersAPI.getUser)
        navigate("/")
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
                            name="passwordConfirm" 
                            value={credentials.passwordConfirm}
                            onChange={handleChange}
                            required></input>
                    </div>
                    <button className=' text-cardamom bg-moonlight hover:bg-land hover:text-vanilla py-1 px-1 rounded mt-5 mb-5' 
                        type="submit" 
                        
                        >SIGN UP</button>
                </form>

            </div>
        </>
    )
}

// 'midnight': '#091123',
// 'afterhour':'#212A3E',
// 'moonlight':'#F1F6F9',
// 'regal': '#34172D',
// 'lining':'#d678a4',