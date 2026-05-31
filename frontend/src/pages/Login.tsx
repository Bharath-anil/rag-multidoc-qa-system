import { useState } from "react"
import api from "../services/api"
import { useNavigate } from "react-router-dom"
import AuthForm from "../components/AuthForm"
import { toast } from "sonner"

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
            localStorage.setItem("username", username)
            toast.success("login sucessful",{ position: "top-right" })    
            navigate("/dashboard")
        }
        catch(error){
            console.log(error)
            toast.error("login failed",{ position: "top-right" })
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
                footerText="Don't have an account?"
                footerLinkText="Register"
                footerLinkTo="/register"
                />
    )
}

export default Login