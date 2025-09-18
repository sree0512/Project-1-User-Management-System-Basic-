import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route, Link } from "react-router-dom"
// import './index.css'
import App from './App.jsx'
import RegisterForm from './components/RegisterForm'
import LoginForm from './components/LoginForm'
import ProfilePage from './components/ProfilePage'

createRoot(document.getElementById('root')).render(
  <BrowserRouter>
    <App />
    <Routes>
      <Route path="/register" element={<RegisterForm />}/>
      <Route path="/login" element={<LoginForm />}/>
      <Route path="/user/profile" element ={<ProfilePage />}/>
    </Routes>
  </BrowserRouter>
)
