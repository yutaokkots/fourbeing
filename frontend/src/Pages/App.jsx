
import { Routes, Route } from 'react-router-dom'
import Dashboard from './Dashboard/Dashboard'

import { useReducer, useState, createContext, useEffect } from 'react'
import AuthPage from './AuthPage/AuthPage'
import Profile from './Profile/Profile'

import './App.css'
import * as usersAPI from '../utilities/users-service'


export const AuthContext = createContext()

const initialState = {
    isAuthenticated: false,
    user: null
}

const reducer = (state, action) => {
    // switches between the two states, login and logout
    switch (action.type) {
        case "LOGIN":
            return {
                ...state,
                isAuthenticated: true,
                user: action.payload.user,
            };
        case "LOGOUT":
            return {
            ...state,
            isAuthenticated: false,
            user: null
            };
        default:
            return state;
    }
  };


export default function App() {
    const [userState, dispatch] = useReducer(reducer, initialState)
    const [user, setUser] = useState(usersAPI.getUser)

    useEffect(()=>{
        setUser(usersAPI.getUser)
    }, [])
    function updateUser(userState){
        setUser(userState)
      }


    return (
        <>
            <AuthContext.Provider value={{user, setUser}}>
                <Routes>
                        <Route path='/' element={<Dashboard user={ user }/>} />
                        <Route path='/login' element={<AuthPage user={ user } setUser={ setUser}/>} />
                        <Route path='/profile' element={<Profile user={ user } setUser={ setUser}/>} />
                    
                </Routes>
            </AuthContext.Provider>
        </>
    )
}




// <h1 className="text-2xl font-bold underline text-blue-600 ">
// Hello world!
// </h1>
// <div>

// </div>
// <h1>Vite + React</h1>
// <div className="card">
// <button onClick={() => setCount((count) => count + 1)}>
//   count is {count}
// </button>
// <p>
//   Edit <code>src/App.jsx</code> and save to test HMR
// </p>
// </div>
// <p className="read-the-docs">
// Click on the Vite and React logos to learn more
// </p>