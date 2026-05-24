import { useState, useEffect } from "react"
import api from "../services/api"
function Dashboard() {

    const [file, setFile] = useState<File | null>(null)
    const [loading, setLoading] = useState(false)
    const [question, setQuestion] = useState("")
    const [answer, setAnswer] = useState("")
    const [asking, setAsking] = useState(false)
    const [documents, setDocuments] = useState<any[]>([])

    //Upload function
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
            fetchDocuments()
        } catch (error) {

            console.log(error)
            setLoading(false)
            alert("Upload failed")
        }
    }

    //Question function
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

    // get all document 
    const fetchDocuments = async () => {

        try {

            const token = localStorage.getItem("token")

            const response = await api.get(
            "/documents",
            {
                headers: {
                Authorization: `Bearer ${token}`
                }
            }
            )

            console.log(response.data)

            setDocuments(response.data)

        } catch (error) {

            console.log(error)
        }
    }

    useEffect(() => {

    fetchDocuments()

    }, [])


    //delete function
    const handleDelete =async(documentId:string)=>{
        try{
            const token =localStorage.getItem("token")

            await api.delete("/documents/delete",
            {
                headers:{
                    Authorization:`Bearer ${token}`
                },
                data: {
                    document_id: documentId
                }
            }
        )
        
        setDocuments((prevDocuments: any[]) =>
            prevDocuments.filter(
                (doc: any) => doc.id !== documentId
            )
        )

        } catch (error) {

            console.log(error)

            alert("Delete failed")
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

                <h2>Uploaded Documents</h2>

                {   
                    documents.map((doc:any)=>(
                        <div key={doc.id}>
                            <p>{doc.filename}</p>
                            <button onClick={() => handleDelete(doc.id)} >
                                Delete
                            </button>
                        </div>
                    ))
                }

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