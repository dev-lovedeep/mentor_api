import {API} from './backend'

export const signup = regno => {
    return fetch(`${API}/signup/${regno}` , {
        method: 'GET'
    })
    .then(response => {
        return response.json()
    })
    .catch(err => console.log(err))
}

export const createAcc = user => {
    return fetch(`${API}/onboard`, {
        method: 'POST',
        headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json'
        },
        body: user
    })
    .then(response => {
        return response.json()
    })
}

export const login = (regno, pass) => {
    const data = {username: regno, password: pass}
    return fetch(`${API}/login/` , {
        method: 'POST',
        headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        return response.json()
    })
}