import axios from "axios"
import { toast } from "sonner"

const api = axios.create({
  baseURL: "http://localhost:8000",
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token")

  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }

  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("token")

      // Prevent redirect loop if already on login
      if (window.location.pathname !== "/") {
        toast.error("Session expired. Please login again.", { position: "top-right" })
        window.location.href = "/login"
      }
    }

    return Promise.reject(error)
  }
)



export default api