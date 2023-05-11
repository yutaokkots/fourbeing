import React, { useState, useContext} from 'react'
import { useNavigate } from 'react-router-dom'
import * as userService from '../../utilities/users-service'
import { AuthContext } from "../../Pages/App"

const initialState = {
    username: '',
    password: ''
}

export default function LoginForm() {
    const { user, setUser } = useContext(AuthContext)
    const [credentials, setCredentials] = useState(initialState);
    const [error, setError] = useState('');
    const navigate = useNavigate()
    
    function handleChange(evt) {
        setCredentials({ ...credentials, [evt.target.name]: evt.target.value });
        setError('');
        }
    
    async function handleSubmit(evt) {
        evt.preventDefault();
        try {
            const userInfo = await userService.login(credentials);
            setUser(userInfo);
        } catch {
            setError('Log In Failed - Try Again');
        }
        navigate("/")
    }

  


    return (
        <>
            <div className="rounded-md m-5 bg-afterhour text-lining">
                    <form autoComplete="off" onSubmit={handleSubmit}>
                    <div className='relative flex-row justify-between  mt-2 mb-2'>
                        <div><label>Username</label></div>
                        <div><input className='text-cardamom' type="text" name="username" value={credentials.login} onChange={handleChange} required /></div>
                    </div>

                    <div className='relative  flex-row justify-between'>
                        <div><label>Password</label></div>
                        <div><input className='text-cardamom' type="password" name="password" value={credentials.password} onChange={handleChange} required /></div>
                    </div>
                    <button className=' text-cardamom bg-vanilla hover:bg-land hover:text-vanilla py-1 px-1 rounded mt-5 mb-5' type="submit">LOG IN</button>
                    </form>

                <p className="error-message">&nbsp;{error}</p>
            </div>
        
        </>
    )
}



