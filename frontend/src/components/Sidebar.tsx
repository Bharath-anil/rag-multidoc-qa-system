import { useState, useEffect,useRef } from "react"
import api from "../services/api"
import {
  PanelLeft,
  FileText,
  Upload,
} from "lucide-react"

type SidebarProps = {
  sidebarOpen: boolean
  setSidebarOpen: React.Dispatch<React.SetStateAction<boolean>>
}



function Sidebar({
  sidebarOpen,
  setSidebarOpen,
}: SidebarProps) {

  const [file, setFile] = useState<File | null>(null)
  const [documents, setDocuments] = useState<any[]>([])
  const [loading, setLoading] = useState(false)
  const fileInputRef = useRef<HTMLInputElement | null>(null)
  // Fetch documents
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

      setDocuments(response.data)

    } catch (error) {

      console.log(error)
    }
  }

  // Delete document
  const handleDelete = async (documentId: string) => {

    try {

      const token = localStorage.getItem("token")

      await api.delete(
        "/documents/delete",
        {
          headers: {
            Authorization: `Bearer ${token}`
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

  // Upload PDF
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

  useEffect(() => {
    fetchDocuments()
  }, [])

  return (

    <div
      className={`
        flex flex-col h-full p-4 transition-all duration-300
        ${sidebarOpen ? "w-96" : "w-20"}
      `}
    >

      {/* Top Section */}
      <div>

        <div className="flex items-center justify-between mb-6">

          {sidebarOpen && (
            <h1 className="text-3xl font-bold">
              AI Assistant
            </h1>
          )}

          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="text-zinc-400 hover:text-white"
          >
            <PanelLeft size={20} />
          </button>

        </div>

       <div>
            <div className={`
                            overflow-hidden transition-all duration-300
                            ${sidebarOpen ? "max-h-40 opacity-100 mt-3" : "max-h-0 opacity-0"}
                        `} >

                        <div className="flex gap-2">

                            <label className="flex-1">

                            <div className="bg-zinc-800 hover:bg-zinc-700 transition-colors rounded-xl p-3 text-sm text-zinc-300 cursor-pointer text-center truncate">
                                {file ? file.name : "Choose PDF"}
                            </div>

                            <input
                                ref={fileInputRef}
                                type="file"
                                accept=".pdf"
                                className="hidden"
                                onChange={(e) => {
                                if (e.target.files) {
                                    setFile(e.target.files[0])
                                }
                                }}
                            />

                            </label>

                            <button
                            onClick={handleUpload}
                            className="bg-white text-black rounded-xl px-4 flex items-center justify-center"
                            >
                            <Upload size={18} />
                            </button>

                        </div>

                        </div>

                        {!sidebarOpen && (

                        <button
                            onClick={() => fileInputRef.current?.click()}
                            className="bg-zinc-800 hover:bg-zinc-700 transition-colors rounded-xl p-3 flex justify-center mt-3"
                            title="Choose PDF"
                        >
                            <Upload size={18} />
                        </button>

                        )}
      </div>
    </div>
      {/* Documents */}
      <div className="mt-8 flex-1 overflow-y-auto">

        {sidebarOpen && (
          <h2 className="text-sm text-zinc-400 mb-3">
            Documents
          </h2>
        )}

        <div className="space-y-2">

          {documents.map((doc: any) => (

            <div
                key={doc.id}
                className="bg-zinc-800 hover:bg-zinc-700 transition-colors p-4 rounded-xl flex items-center justify-center"
                title={doc.filename}
            >

                {sidebarOpen ? (

                <>
                    <span
                    className="truncate text-sm font-medium flex-1"
                    >
                    {doc.filename}
                    </span>

                    <button
                    className="text-red-400 hover:text-red-300 text-xs"
                    onClick={() => handleDelete(doc.id)}
                    >
                    Delete
                    </button>
                </>

                ) : (

                <FileText size={18} />

                )}

            </div>

            ))}

        </div>

      </div>

    </div>
  )
}

export default Sidebar