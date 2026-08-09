import { useState } from "react"
import api from "../services/api"
import AuthForm from "../components/AuthForm"
import { toast } from "sonner"
import { useNavigate } from "react-router-dom"

function Register(){
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const navigate = useNavigate()

    const handleRegister = async () =>{
        try{
            const response =await api.post("/register",{
                username,
                password
            })
            console.log(response.data)
            toast.success("User registered Sucessfully",{ position: "top-right" })
            navigate("/")
        }
        catch (error: any) {
            const errors = error.response?.data?.errors

            if (errors?.length > 0) {
                toast.error(errors[0].msg, {
                position: "top-right",
                })
            } else {
                toast.error(
                error.response?.data?.message || "Registration failed",
                { position: "top-right" }
                )
            }
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
                minPasswordLength={8}
                description="Username: 3–30 characters, no spaces. Password: minimum 8 characters."
                />
   )
}

export default Register