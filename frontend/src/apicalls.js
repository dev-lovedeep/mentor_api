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
        if(response.status === 200){
            return response.json()
        }else{
            return ""
        }
    })
    .catch(err => {
        console.log(err)
    })
}