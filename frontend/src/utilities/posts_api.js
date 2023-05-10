
const BASE_URL = "http://localhost:8000/api/topic"


export default async function sendRequest(url, method = 'GET', payload = null) {
    const options = { method };
    if (payload) {
        options.headers = { 'Content-Type': 'application/json' };
        options.body = JSON.stringify(payload);
    }

    const res = await fetch(url, options);
    if (res.ok) return res.json();
    throw new Error('Bad Request')

    
}

export function getPost(){
    return sendRequest(`${BASE_URL}/test/`)
}


// return fetch(url, options).then((response) => {
//     return response.json()
// }).catch((err) => {
//     throw new Error('Bad Request', err);
// })