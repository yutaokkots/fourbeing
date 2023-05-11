import * as usersAPI from './users-api'


// export async function signUp(userData){
//     let loginData = {
//         username: userData.username,
//         password: userData.password
//     }
 

//     await usersAPI.signUp(userData).then((response) => {
//         console.log(response.token)
//         console.log(response)
//         console.log("here")
//         if (response.token === "getToken"){
//             // let loginData = {...userData}
//             // delete loginData.email
//             // delete loginData.passwordConfirm
//             console.log(loginData)
//             return usersAPI.login(loginData)
//         }}).then((token) => {
//             localStorage.setItem('token', token.token.access);
//         })

//     //localStorage.setItem('token', token.token.access);
//     return getUser()
// }

export async function signUp(userData){
    let loginData = {
        username: userData.username,
        password: userData.password
    }
    try {
        const response = await usersAPI.signUp(userData);
        if (response.token === "getToken") {
            const tokenResponse = await usersAPI.login(loginData);
            localStorage.setItem('token', tokenResponse.access);
        }
        return getUser();
    } catch (error) {
        console.error(error);
        // Handle error here
    }
}


// getToken() -> gets token from localhost storage (if there)
export function getToken(){
    const token = localStorage.getItem("token");
    console.log(`here is the token ${token}`)
    if (!token) return null;

    const payload = JSON.parse(window.atob(token.split('.')[1]));
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
    localStorage.setItem('token', token.access);
    return getUser()
}

export function logOut() {
    localStorage.removeItem('token');
}
