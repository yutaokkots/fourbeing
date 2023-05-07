

const BASE_URL = "http://localhost:8000/api"


export default async function sendRequest(url, method = 'GET', payload = null) {
    const options = { method };
    if (payload) {
        options.headers = { 'Content-Type': 'application/json' };
        options.body = JSON.stringify(payload);
    }
    console.log("(1) sendRequest function triggered")
    
    const res = await fetch(url, options);
    
    
    console.log("(2), at res", res)
    if (res.ok) return res.json();

    throw new Error('Bad Request').catch((error) => console.log(error))

}

export function getPost(){
    
    return sendRequest(`${BASE_URL}/test/`)
}