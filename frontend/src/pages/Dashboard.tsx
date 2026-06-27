import { useState,useEffect } from "react"
import DashboardLayout from "../components/DashboardLayout"
import Sidebar from "../components/Sidebar"
import ConversationSidebar from "../components/ConversationSidebar"
import ChatArea from "../components/ChatArea"
import api from "../services/api"

type Message = {
  role: "user" | "assistant"
  content: string
}
function Dashboard() {
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [conversations, setConversations] = useState([])
  const [activeConversationId, setActiveConversationId] =useState<string | null>(null)
  const [messages, setMessages] = useState<Message[]>([])


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
      fetchConversations()
    }, [])

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
  

  return (
    <DashboardLayout
        sidebarOpen={sidebarOpen}
        sidebar={
          <ConversationSidebar
            conversations={conversations}
            activeConversationId={  activeConversationId }
            onSelectConversation={ setActiveConversationId }
            onNewChat={handleNewChat}
          />
            // <Sidebar
            //     // sidebarOpen={sidebarOpen}
            //     // setSidebarOpen={setSidebarOpen}
            // />
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