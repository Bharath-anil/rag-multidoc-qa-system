import { useState, useEffect,useRef } from "react"
import api from "../services/api"
import { PanelLeft, FileText, Upload} from "lucide-react"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription} from "./ui/dialog"
import { toast } from "sonner"
import { useNavigate } from "react-router-dom"
import ConversationSidebar from "../components/ConversationSidebar"
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger,SheetDescription}from "./ui/sheet"
import { Button } from "./ui/button"
import { Trash2, Loader2 } from "lucide-react"

type Conversation = {
  id: string
  title: string
  updated_at: string
}

type SidebarProps = {
  sidebarOpen: boolean
  setSidebarOpen: React.Dispatch< React.SetStateAction<boolean>>
  conversations: Conversation[]
  activeConversationId: string | null
  onSelectConversation: (id: string) => void
  handleDeleteConversation: ( id: string) => void
  onNewChat: () => void
  deletedConversations: Conversation[]
  handleRestoreConversation: ( id: string ) => void
  // refreshDeletedConversations: () => void
}


function Sidebar({
  sidebarOpen,
  setSidebarOpen,
  conversations,
  activeConversationId,
  onSelectConversation,
  handleDeleteConversation,
  onNewChat,
  deletedConversations,
  handleRestoreConversation,
  // refreshDeletedConversations
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

      const response = await api.get( "/documents")
      setDocuments(response.data)

    } catch (error) {

      console.log(error)
    }
  }

  // Delete document
  const handleDelete = async (documentId: string) => {

    try {

      await api.delete(`/documents/${documentId}`)
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
      const response = await api.post( "/upload", formData)
      setLoading(false)

      toast.success("PDF uploaded successfully", { position: "top-right" })

      fetchDocuments()

    } catch (error) {

      console.log(error)
      toast.error("Upload failed", { position: "top-right" })
    }finally {
    setLoading(false)
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
    <div className={` flex flex-col h-full p-4 transition-all duration-300 overflow-hidden
        ${sidebarOpen ? "w-96" : "w-20"} 
      `}
    >

      {/* Top Section */}
      <div>

        <div className="flex items-center justify-between mb-6">

          {sidebarOpen && (
            <h1 className="text-3xl font-bold">
              DocMind AI
            </h1>
          )}

          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="text-zinc-400 hover:text-white"
          >
            <PanelLeft size={20} />
          </button>

        </div>
          <div className ="border-b border-zinc-800">
              <ConversationSidebar
              conversations={conversations}
              activeConversationId={activeConversationId}
              onSelectConversation={onSelectConversation}
              handleDeleteConversation={handleDeleteConversation}
              onNewChat={onNewChat}
              sidebarOpen={sidebarOpen} 
            />
        </div>

       <div>
            <div className={`
                            overflow-hidden transition-all duration-300
                            ${sidebarOpen ? "max-h-40 opacity-100 mt-3" : "max-h-0 opacity-0"}
                        `} >

                        <div className="flex gap-2">

                            <label className="flex-1">

                            <div className={`bg-zinc-800 rounded-xl p-3 text-sm text-zinc-300 text-center truncate ${loading ? "opacity-50 cursor-not-allowed" : "hover:bg-zinc-700 cursor-pointer"}`}>
                                {file ? file.name : "Choose PDF"}
                            </div>

                            <input
                                ref={fileInputRef}
                                type="file"
                                accept=".pdf"
                                disabled={loading}
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
                            disabled={loading}
                            className="bg-white text-black rounded-xl px-4 flex items-center justify-center"
                            >
                             {loading ? (
                                  <Loader2 size={18} className="animate-spin" />
                                ) : (
                                  <Upload size={18} />
                                )}
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

      {/* Documents */}
      <div className="mt-8 flex-1 overflow-y-auto ">
        
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
      
      <Sheet>
        <SheetTrigger asChild>
          <Button
            variant="outline"
           className={`mt-4 ${ sidebarOpen ? "w-full" : "w-full justify-center" }`}
          //  onClick={refreshDeletedConversations}
          >
            <Trash2 className="mr-2 h-4 w-4" />

            {sidebarOpen && "Recycle Bin"}
          </Button>
        </SheetTrigger>
            <SheetContent className="bg-zinc-950 text-white">
              <SheetHeader>
                <SheetTitle>
                  Deleted Conversations
                </SheetTitle>

                <SheetDescription>
                  Restore previously deleted conversations.
                </SheetDescription>
              </SheetHeader>

              <div className="mt-6">
                <p className="mb-4">
                  Count: {deletedConversations.length}
                </p>

                {deletedConversations.map((conversation) => (
                  <div
                    key={conversation.id}
                    className="mb-3 p-3 border border-zinc-700 rounded"
                  >
                    <p>{conversation.title}</p>

                    <Button
                      size="sm"
                      className="mt-2"
                      onClick={() =>
                        handleRestoreConversation(
                          conversation.id
                        )
                      }
                    >
                      Restore
                    </Button>
                  </div>
                ))}
              </div>
            </SheetContent>
      </Sheet>

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

            <div className="flex justify-end gap-2 mt-4">
              <Button variant="outline" onClick={() => setShowDeactivateDialog(false)}>
                Cancel
              </Button>

              <Button
                variant="destructive" onClick={handleDeactivate}>
                Deactivate
              </Button>
            </div>


          </DialogContent>
        </Dialog>
        </div>
   </>
  )
  
}

export default Sidebar