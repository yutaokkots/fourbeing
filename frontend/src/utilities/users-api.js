
const BASE_URL = 'http://localhost:8000/api/auth'
import { getToken } from './users-service'



export default async function sendRequest(url, method = 'GET', payload = null) {
    const options = { method };
    if (payload) {
        options.headers = { 'Content-Type': 'application/json' };
        options.body = JSON.stringify(payload);
    }

    const token = getToken();
    if(token){
        options.headers = options.headers || {};
        options.headers.Authorization = `Bearer ${token}`;
    }  

    const res = await fetch(url, options);
    if (res.ok) return res.json();
    throw new Error('Bad Request')
    
}

export function login(userData){
    return sendRequest(`${BASE_URL}/login/`, 'POST', userData)
}

export function signUp(userData){
    return sendRequest(`${BASE_URL}/createuser/`, 'POST', userData)
}