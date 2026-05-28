import { useState } from "react"
import api from "../services/api"
import { useNavigate } from "react-router-dom"
import AuthForm from "../components/AuthForm"

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
        <AuthForm
                title="Login"
                username={username}
                password={password}
                setUsername={setUserName}
                setPassword={setPassword}
                handleSubmit={handleLogin}
                buttonText="Login"
                />
    )
}

export default Login