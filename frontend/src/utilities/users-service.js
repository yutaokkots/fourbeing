import * as usersAPI from './users-api'


export async function signUp(userData){
    const token = await usersAPI.signUp(userData);
    console.log(token)
    localStorage.setItem('token', token.token);
    return getUser()
}

// getToken() -> gets token from localhost storage (if there)
export function getToken(){
    const token = localStorage.getItem("token");
    if (!token) return null;
    const payload = JSON.parse(window.atob(token.split('.')[1]));
    console.log(payload)
    if (payload.exp < Date.now() / 1000) {
        localStorage.removeItem('Token');
        return null;
    }
    return token;
}

// getUser() -> returns token 
export function getUser(){
    const token = getToken();
    return token ? JSON.parse(window.atob(token.split('.')[1])).name : null
}

export async function login(credentials){
    const token = await usersAPI.login(credentials);
    console.log(token)
    localStorage.setItem('token', token.access);
    return getUser()
}