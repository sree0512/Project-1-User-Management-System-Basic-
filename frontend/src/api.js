
import axios from 'axios';
import { data } from 'react-router-dom';

const BASE_URL = "http://127.0.0.1:5000"; //Flask backend

const axiosInstance = axios.create({ 
    baseURL: BASE_URL,
    timeout: 5000,
    headers: {
        'Content-type': 'Application/json',
        // 'Authorization': 'Bearer YOUR_AUTH_TOKEN',
    }, 
});

// Request interceptors 
axiosInstance.interceptors.request.use(
    (config) => {
        //add an authorization token from localStorage or a cookie
        const token = localStorage.getItem("token")
        if(token){
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        // Handle request errors
        return Promise.reject(error);
    }
)

// Define and export api functions
export const register = (data) => axiosInstance.post('/register', data).then(res => res.data)
export const login = (data) => axiosInstance.post('/login', data).then(res => res.data)
export const profile = () => axiosInstance.get('/user/profile').then(res => res.data)
export const updateUser = (data) => axiosInstance.put('/user/update', data).then(res => res.data)
export const changePassword = (data) => axiosInstance.put('/user/change-password', data).then(res => res.data)
export const deleteUser = () => axiosInstance.delete('/user/delete').then(res => res.data)



/*
export const register = async (data) => {
    try {
        const res = await axiosInstance.post('/register', data)
        return res.data
    } catch(err) {
        throw err.response?.data || { error: "Network error" }
    }
}*/