import axios from "axios"

const HOST = "http://127.0.0.1:8000"

export const endpoints = {
    'categories': '/categories/',
    'tours': '/tours/'
}

export const authApi = () => {
    return axios.create({
        baseURL: HOST,
        headers: {
            'Authorization': 'Bearer ...'
        }
    })
}

export default axios.create({
    baseURL: HOST
})