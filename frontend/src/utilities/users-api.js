
const BASE_URL = 'http://localhost:8000/api/auth'
import sendRequest from './send-requests'



export function login(userData){
    console.log('user-service', userData)
    return sendRequest(`${BASE_URL}/signin/`, 'POST', userData)
}

export function signUp(userData){
    
    return sendRequest(`${BASE_URL}/createuser/`, 'POST', userData)
}

// export function logout(userData){
//     return sendRequest(`${BASE_URL}/createuser/`, 'POST', userData)
// }