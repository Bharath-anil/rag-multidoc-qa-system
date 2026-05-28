import { useState } from "react"
import DashboardLayout from "../components/DashboardLayout"
import Sidebar from "../components/Sidebar"
import ChatArea from "../components/ChatArea"

function Dashboard() {
  const [sidebarOpen, setSidebarOpen] = useState(true)

  return (
    <DashboardLayout
        sidebarOpen={sidebarOpen}
        sidebar={
            <Sidebar
                sidebarOpen={sidebarOpen}
                setSidebarOpen={setSidebarOpen}
            />
        }
    >
       <ChatArea />
    </DashboardLayout>
  )
}


export default Dashboard