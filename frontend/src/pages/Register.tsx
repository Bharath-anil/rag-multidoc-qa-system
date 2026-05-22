import { useState } from "react"
import api from "../services/api"

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
        <div>
            <h1>Register</h1>

            <input
                type="text"
                placeholder="Enter User Name"
                value={username}
                onChange={(e)=> setUsername(e.target.value)}
            />
                
            <br />
            <br />

            <input
                type="password"
                placeholder="Enter password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />

            <br />
            <br />

            <button onClick={handleRegister}>Register</button>


        </div>
   )
}

export default Register