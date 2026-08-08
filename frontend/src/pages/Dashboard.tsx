import { useState,useEffect } from "react"
import DashboardLayout from "../components/DashboardLayout"
import Sidebar from "../components/Sidebar"
import ChatArea from "../components/ChatArea"
import api from "../services/api"
import { toast } from "sonner"
import { Menu } from "lucide-react"
import { Sheet, SheetContent, SheetTrigger} from "@/components/ui/sheet"
type Message = {
  role: "user" | "assistant"
  content: string
  sources?: string[]
}
function Dashboard() {
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [conversations, setConversations] = useState([])
  const [activeConversationId, setActiveConversationId] =useState<string | null>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [deletedConversations, setDeletedConversations] = useState([])
  const [isMobile, setIsMobile] = useState(false)
  const fetchConversations = async () => {
    try {
      const response = await api.get("/conversations")

      setConversations(response.data)

      if (
        response.data.length > 0 &&
        !activeConversationId
      ) {
        setActiveConversationId(
          response.data[0].id
        )
      }
    } catch (error) {
      console.error(error)
    }
  }

  const fetchMessages = async ( conversationId: string ) => {
    try {
      const response = await api.get(
        `/messages/${conversationId}`
      )
      setMessages(response.data)  
    } catch (error) {
      console.error(error)
    }
  }



  useEffect(() => {
      if (!activeConversationId) return
      fetchMessages(activeConversationId) }, [activeConversationId])
  
  useEffect(() => {
    const checkScreen = () => {
      setIsMobile(window.innerWidth < 768)
    }

    checkScreen()

    window.addEventListener("resize", checkScreen)

    return () =>
      window.removeEventListener("resize", checkScreen)
  }, [])
  const handleNewChat = async () => {
    try {
      const response = await api.post(
        "/conversations"
      )

      const newConversation = response.data

      setConversations(prev => [
        newConversation,
        ...prev,
      ])

      setActiveConversationId(
        newConversation.id
      )

      setMessages([])
    } catch (error) {
      console.error(error)
    }
  }
  
  const handleDeleteConversation = async ( conversationId: string ) => {
    try {
      await api.delete(  `/conversations/${conversationId}` )

      setConversations(prev =>  prev.filter( c => c.id !== conversationId )  )

      if ( activeConversationId === conversationId  ) {
        setActiveConversationId(null)
        setMessages([])
      }
      fetchDeletedConversations()
      toast.warning( "Conversation moved to recycle bin", { position: "top-right" } )
    } catch (error) {
      console.log(error)
      toast.error( "Failed to delete conversation", { position: "top-right" } )
    }
  }
    
  const fetchDeletedConversations = async () => {
    try {
      const response = await api.get(
        "/conversation/deleted"
      )
      setDeletedConversations(response.data)
    } catch (error) {
      console.error(error)
    }
  }

  const handleRestoreConversation = async (  conversationId: string ) => {
    try {
      await api.post(`/conversation/${conversationId}/restore`)
      await fetchConversations()
      await fetchDeletedConversations()

      setActiveConversationId(
        conversationId
      )
      toast.success( "Conversation restored", {  position: "top-right"})
      } catch {
          toast.error("Restore failed",{position: "top-right"})
        }
    }
  
  useEffect(() => {
    fetchConversations()
    fetchDeletedConversations()
  }, [])

  return (
    <DashboardLayout
      sidebarOpen={sidebarOpen}
      sidebar={
        !isMobile && (
          <Sidebar
            sidebarOpen={sidebarOpen}
            setSidebarOpen={setSidebarOpen}
            conversations={conversations}
            activeConversationId={activeConversationId}
            onSelectConversation={setActiveConversationId}
            handleDeleteConversation={handleDeleteConversation}
            onNewChat={handleNewChat}
            deletedConversations={deletedConversations}
            handleRestoreConversation={handleRestoreConversation}
            refreshDeletedConversations={fetchDeletedConversations}
            isMobile={false}
          />
        )
      }
    >

      <Sheet>
        <SheetTrigger asChild>
          <button className="md:hidden p-2">
            <Menu size={22} />
          </button>
        </SheetTrigger>

        <SheetContent  side="left" className="p-0 w-[100vw] bg-zinc-900 text-white" >
          <Sidebar
            sidebarOpen={true}
            setSidebarOpen={setSidebarOpen}
            conversations={conversations}
            activeConversationId={activeConversationId}
            onSelectConversation={setActiveConversationId}
            handleDeleteConversation={handleDeleteConversation}
            onNewChat={handleNewChat}
            deletedConversations={deletedConversations}
            handleRestoreConversation={handleRestoreConversation}
            refreshDeletedConversations={fetchDeletedConversations}
            isMobile={true}
          />
        </SheetContent>
      </Sheet>

      <ChatArea
          messages={messages}
          setMessages={setMessages}
          activeConversationId={
            activeConversationId
          }
        />
    </DashboardLayout>
  )
  }


export default Dashboard