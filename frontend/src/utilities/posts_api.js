import sendRequest from "./send-requests"

const BASE_URL = "http://localhost:8000/api/fourbeing/"

export function getPostAll(){
    return sendRequest(`${BASE_URL}`)
}

export function getPost(){
    return sendRequest(`${BASE_URL}/:id`)
}

export function createPost(){
    return sendRequest(`${BASE_URL}create/`)
}

export function deletePost(){
    return sendRequest(`${BASE_URL}create/`)
}

export function updatePost(){
    return sendRequest(`${BASE_URL}create/`)
}




// return fetch(url, options).then((response) => {
//     return response.json()
// }).catch((err) => {
//     throw new Error('Bad Request', err);
// })