import { useState } from "react"
import api from "../services/api"
import AuthForm from "../components/AuthForm"
import { toast } from "sonner"
function Register(){
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")


    const handleRegister = async () =>{
        try{
            const response =await api.post("/register",{
                username,
                password
            })
            console.log(response.data)
            toast.success("User registered Sucessfully",{ position: "top-right" })
        }
        catch (error){
            console.log(error)
            toast.error("Registeration failed",{ position: "top-right" })
        }
    }

    return (
            <AuthForm
                title="Register"
                username={username}
                password={password}
                setUsername={setUsername}
                setPassword={setPassword}
                handleSubmit={handleRegister}
                buttonText="Register"
                footerText="Already have an account?"
                footerLinkText="Login"
                footerLinkTo="/"
                />
   )
}

export default Register