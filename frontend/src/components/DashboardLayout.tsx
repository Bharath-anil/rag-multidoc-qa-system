type DashboardLayoutProps = {
  sidebar: React.ReactNode
  children: React.ReactNode
  sidebarOpen: boolean
}

function DashboardLayout({
  sidebar,
  children,
  sidebarOpen,
}: DashboardLayoutProps) {

  return (

    <div className="h-screen bg-zinc-950 text-white flex overflow-hidden">

      <aside
        className={`
          border-r border-zinc-800 bg-zinc-900
          transition-all duration-300
          ${sidebarOpen ? "w-96" : "w-20"}
        `}
      >
        {sidebar}
      </aside>

      <main className="flex-1 flex flex-col overflow-hidden">
        {children}
      </main>

    </div>

  )
}

export default DashboardLayout