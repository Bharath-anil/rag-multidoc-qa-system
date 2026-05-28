import { useState } from "react"
import api from "../services/api"
import AuthForm from "../components/AuthForm"

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
            alert("User registered Sucessfully")
        }
        catch (error){
            console.log(error)
            alert("Registeration failed")
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
                />
   )
}

export default Register