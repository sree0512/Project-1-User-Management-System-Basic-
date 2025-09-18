import { register } from "../api";

import { useState } from "react"; //to handle form input and error messages
import { useNavigate } from "react-router-dom"; //to redirect to login after successful registration
export default RegisterForm;


function RegisterForm(){
    //Hooks like useState and useNavigate cannot be called outside a function component.
    // hooks here: useState, useNavigate
    const [username, setUsername] = useState("");
    const [email, setEmail]= useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const navigate = useNavigate();

    // handleSubmit here
    const handleSubmit = async (e) => {
        e.preventDefault(); //prevent page refresh
        try {
            const res = await register({ username, email, password });
            console.log("Registered:", res)
            navigate("/login"); //redirect after success
        } catch (err) {
            setError(err.error || "Registration failed")    
        }
    }
    // return JSX form
    return(
        <form onSubmit = {handleSubmit}>
            <input type="text" placeholder = "Username" value={username} onChange={e => setUsername(e.target.value)}/>
            <input type="email" placeholder = "email" value={email} onChange={e => setEmail(e.target.value)}/>
            <input type="password" placeholder="password" value={password} onChange={e => setPassword(e.target.value)}/>
            <button type="submit">Register</button>
            {error && <p style={{color: "red" }}>{error}</p>}
        </form>
        )

}