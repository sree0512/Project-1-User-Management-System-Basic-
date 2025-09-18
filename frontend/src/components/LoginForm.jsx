import { login } from "../api";
export default LoginForm;
import { useNavigate } from "react-router-dom";
import { useState } from "react";


function LoginForm(){
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [isChecked, setIsChecked] = useState(false);
    const handleChange = () => setIsChecked(!isChecked)
    
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const res = await login({ email, password });
            console.log("Login response:", res);
            const access_token = res.access_token
            localStorage.setItem("token", access_token)
            navigate("/user/profile")
        }
        catch (err){
            setError(err.error || "Login failed")
        }
    }
    return (
        <form onSubmit = {handleSubmit}>
            <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)}/>
            <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)}/>
            <button type="submit">Login</button>
            {error && <p style={{color: "red" }}>{error}</p>}
            <label>
                <input type="checkbox" placeholder="Remember me" checked={isChecked} onChange={handleChange} />
                Remember me
            </label>
        </form>
    )
}



/*
User enters email & password

handleSubmit calls login() from api.js

On success → store JWT in localStorage

Redirect to /user/profile using navigate()

On failure → set error state and display*/
