import { useState,useEffect } from "react"
import DashboardLayout from "../components/DashboardLayout"
import Sidebar from "../components/Sidebar"
import ChatArea from "../components/ChatArea"
import api from "../services/api"
import { toast } from "sonner"

type Message = {
  role: "user" | "assistant"
  content: string
}
function Dashboard() {
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [conversations, setConversations] = useState([])
  const [activeConversationId, setActiveConversationId] =useState<string | null>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [deletedConversations, setDeletedConversations] = useState([])

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
      toast.success( "Conversation moved to recycle bin", { position: "top-right" } )
    } catch (error) {
      toast.error( "Failed to delete conversation", { position: "top-right" } )
    }
  }
    
  const fetchDeletedConversations = async () => {
    try {
      const response = await api.get(
        "/conversation/deleted"
      )
      console.log(
  "Sidebar deleted conversations:",
  deletedConversations
)
      setDeletedConversations(response.data)
    } catch (error) {
      console.error(error)
    }
  }

  const handleRestoreConversation = async (  conversationId: string ) => {
    try {
      await api.post(`/conversation/${conversationId}/restore`)
      fetchConversations()
      fetchDeletedConversations()
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
              refreshDeletedConversations={ fetchDeletedConversations}
            />
        }
    >
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