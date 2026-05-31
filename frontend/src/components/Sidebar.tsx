import { useState, useEffect,useRef } from "react"
import api from "../services/api"
import { PanelLeft, FileText, Upload} from "lucide-react"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription} from "./ui/dialog"
import { toast } from "sonner"
import { useNavigate } from "react-router-dom"


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
  const [showDeactivateDialog, setShowDeactivateDialog] = useState(false)
  const fileInputRef = useRef<HTMLInputElement | null>(null)
  const navigate = useNavigate()
  const username = localStorage.getItem("username")
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
        `/documents/${documentId}`,
        {
          headers: {
            Authorization: `Bearer ${token}`
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

      toast.error("Delete failed", { position: "top-right" })
    }
  }

  // Upload PDF
  const handleUpload = async () => {

    if (!file) {
      toast.info("Please select a PDF", { position: "top-right" })
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

      toast.success("PDF uploaded successfully", { position: "top-right" })

      fetchDocuments()

    } catch (error) {

      console.log(error)

      setLoading(false)

      toast.error("Upload failed", { position: "top-right" })
    }
  }

// logout option 
const handleLogout = () => {
  localStorage.removeItem("token")
  navigate("/")
}

// deactivate  option 
const handleDeactivate = () => {
  toast.error( "Account deactivation not implemented yet",{position :"top-right"} )

}

  useEffect(() => {
    fetchDocuments()
  }, [])

  return (
    <>
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
          {documents.length === 0 ? (

          <div className="text-center text-zinc-500 mt-8">

            <div className="text-3xl mb-2">
              📄
            </div>

            {sidebarOpen && (
              <>
                <p>No documents uploaded</p>
                <p className="text-xs mt-1">
                  Upload a PDF to get started
                </p>
              </>
            )}

          </div>

        ) : (
            documents.map((doc: any) => (

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

              ))
          )}
        </div>

      </div>

      {/* Logout section */}
      <div className="border-t border-zinc-800 pt-4 mt-4">

        {sidebarOpen ? (

          <div className="space-y-3">

            <div className="bg-zinc-800 rounded-xl p-3">

              <div className="flex items-center gap-3">

                <div className="w-10 h-10 rounded-full bg-zinc-700 flex items-center justify-center">
                  👤
                </div>

                <div>

                  <p className="font-medium">
                    {username}
                  </p>

                  <p className="text-xs text-zinc-400">
                    AI Assistant User
                  </p>

                </div>

              </div>

            </div>

            <button
              onClick={handleLogout}
              className="w-full bg-zinc-800 hover:bg-zinc-700 rounded-xl p-3"
            >
              Logout
            </button>

            <button onClick={() => setShowDeactivateDialog(true)} className="w-full bg-red-950 hover:bg-red-900 text-red-300 rounded-xl p-3" >
              Deactivate Account
            </button>

          </div>

        ) : (

          <button
            className="w-full bg-zinc-800 rounded-xl p-3"
            title={username || "User"}
          >
            👤
          </button>

        )}

      </div>
    </div>
    <Dialog
          open={showDeactivateDialog}
          onOpenChange={setShowDeactivateDialog}
        >
          <DialogContent className="bg-zinc-900 text-white border border-zinc-800">

          <DialogHeader>

              <DialogTitle>
                Deactivate Account
              </DialogTitle>

              <DialogDescription className="text-zinc-400">
                This action cannot be undone.
                All uploaded documents and chat history
                will be permanently removed.
              </DialogDescription>

            </DialogHeader>

            <div className="flex gap-3 mt-4">

              <button
                onClick={() => setShowDeactivateDialog(false)}
                className="flex-1 bg-zinc-800 hover:bg-zinc-700 rounded-lg p-2"
              >
                Cancel
              </button>

              <button
                onClick={() => {
                  setShowDeactivateDialog(false)
                  handleDeactivate()
                }}
                className="flex-1 bg-red-600 hover:bg-red-500 rounded-lg p-2"
              >
                Confirm
              </button>

            </div>

          </DialogContent>
        </Dialog>
   </>
  )
  
}

export default Sidebar