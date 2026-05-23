import { useState } from "react"
import api from "../services/api"
function Dashboard() {

    const [file, setFile] = useState<File | null>(null)
    const [loading, setLoading] = useState(false)
    const [question, setQuestion] = useState("")
    const [answer, setAnswer] = useState("")
    const [asking, setAsking] = useState(false)

    const handleUpload = async () => {

    if (!file) {
        alert("Please select a PDF")
        return
    }

    try {
        setLoading(true)
        const formData = new FormData()

        formData.append("file", file)

        const token = localStorage.getItem("token")

        const response = await api.post(
        "/upload",
        formData,
        {
            headers: {
            Authorization: `Bearer ${token}`
            }
        }
        )

        console.log(response.data)
        setLoading(false)
        alert("PDF uploaded successfully")
        
    } catch (error) {

        console.log(error)
        setLoading(false)
        alert("Upload failed")
    }
    }

    const handleAsk = async () => {

    if (!question) {
        alert("Enter a question")
        return
    }

    try {

        setAsking(true)

        const token = localStorage.getItem("token")

        const response = await api.post(
        "/ask",
        {
            question
        },
        {
            headers: {
            Authorization: `Bearer ${token}`
            }
        }
        )

        setAnswer(response.data.answer)

        setAsking(false)

    } catch (error) {

        console.log(error)

        setAsking(false)

        alert("Question failed")
    }
    }

    return (
            <div>

                <h1>Dashboard</h1>

                <input
                    type="file"
                    accept=".pdf"
                    placeholder="Select a PDF file"
                    onChange={(e) => {

                    if (e.target.files) {
                        setFile(e.target.files[0])
                    }

                    }}
                />

                <br />
                <br />

                <button onClick={handleUpload}>
                  {loading ? "Uploading..." : "Upload PDF"}
                </button>
                
                <br />
                <br />

                <textarea
                    placeholder="Ask a question"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                />

                <br />
                <br />

                <button onClick={handleAsk}>
                    {asking ? "Thinking..." : "Ask Question"}
                </button>

                <br />
                <br />

                <p>{answer}</p>

            </div>
        )
}

export default Dashboard