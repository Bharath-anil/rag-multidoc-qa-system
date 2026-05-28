import { Routes, Route } from "react-router-dom"
import Login from "./pages/Login"
import Register from "./pages/Register"
import Dashboard from "./pages/Dashboard"
import ProtectedRoute from "./components/ProtectedRoute"
import "./index.css"
function App() {
<div className="bg-black text-white h-screen flex items-center justify-center">
  Tailwind Working
</div>
  return (
    
    <Routes>

      <Route path="/" element={<Login />} />

      <Route path="/register" element={<Register />} />

      <Route path="/dashboard" element={<ProtectedRoute>
                                          <Dashboard />
                                        </ProtectedRoute>} />

    </Routes>
    
  )
}

export default App

