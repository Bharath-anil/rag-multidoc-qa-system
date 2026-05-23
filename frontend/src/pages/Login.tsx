import { useState } from "react"
import api from "../services/api"
import { useNavigate } from "react-router-dom"

function Login(){

    const [username,setUserName] =useState("")
    const [password,setPassword] =useState("")

    const navigate = useNavigate()
    const handleLogin = async() =>{
        try{
            const response = await api.post("/login",{
                username,
                password
            })   
            
            localStorage.setItem("token",response.data.access_token)
            alert("login sucessful")    
            navigate("/dashboard")
        }
        catch(error){
            console.log(error)
            alert("login failed")
        }
    }   

    return (
        <div>
            <h1>Login</h1>

            <input
            type="text"
            placeholder="Enter the username"
            value={username}
            onChange={(e)=>setUserName(e.target.value)}
            />
            <br/>
            <br/>

            <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e)=> setPassword(e.target.value)}
            />
            <br/>
            <br/>

            <button onClick={handleLogin}>Login </button>

        </div>
    )
}

export default Login