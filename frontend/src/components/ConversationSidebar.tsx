import { Plus,MessageSquare,Trash2   } from "lucide-react"
import { useState } from "react"
import { AlertDialog,AlertDialogAction,AlertDialogCancel,AlertDialogContent,AlertDialogDescription,AlertDialogFooter,AlertDialogHeader,AlertDialogTitle,} from "./ui/alert-dialog"

interface Conversation {
  id: string
  title: string
  updated_at: string
}

interface Props {
  conversations: Conversation[]
  activeConversationId: string | null
  onSelectConversation: (id: string) => void
  onNewChat: () => void
  handleDeleteConversation: ( id: string ) => void
  sidebarOpen: boolean
}

function ConversationSidebar({
  conversations,
  activeConversationId,
  onSelectConversation,
  handleDeleteConversation,
  onNewChat,
  sidebarOpen
}: Props) {

  const [conversationToDelete, setConversationToDelete] =
    useState<string | null>(null)

  return (
    <div className="flex flex-col gap-2">
      <button
        onClick={onNewChat}
        className="w-full p-3 mb-4 rounded-lg bg-zinc-800 hover:bg-zinc-700"
      >
       {sidebarOpen ? (   "+ New Chat"  ) : (
            <Plus size={20} />
          )}
      </button>

      <div className={`
          flex flex-col gap-2 overflow-y-auto custom-scrollbar
          ${sidebarOpen ? "max-h-64" : "max-h-64"}
        `}>
        {conversations.map((conversation) => (
          <button
                key={conversation.id}
                onClick={() =>
                  onSelectConversation(conversation.id)
                }
                className={`w-full p-3 rounded-lg transition ${
                  activeConversationId === conversation.id
                    ? "bg-zinc-700"
                    : "hover:bg-zinc-900"
                }`}
              >
                {sidebarOpen ? (
                  <div className="flex items-center justify-between">
                    <span className="truncate">
                      {conversation.title.length > 30
                        ? conversation.title.slice(0, 30) + "..."
                        : conversation.title}
                    </span>

                    <Trash2
                      size={16}
                      className="shrink-0"
                      onClick={(e) => {
                        e.stopPropagation()
                        setConversationToDelete(
                          conversation.id
                        )
                      }}
                    />
                  </div>
                ) : (
                  <div className="flex justify-center">
                    <MessageSquare size={18} />
                  </div>
                )}
              </button>
        ))}
      </div>
      <AlertDialog open={!!conversationToDelete} onOpenChange={() => setConversationToDelete(null) }>
          <AlertDialogContent className="bg-zinc-900 text-white border border-zinc-800">
            <AlertDialogHeader>
              <AlertDialogTitle className="text-lg">
                Delete Conversation?
              </AlertDialogTitle>

              <AlertDialogDescription className="text-zinc-400">
                This conversation will be moved to
                the recycle bin and can be restored
                later.
              </AlertDialogDescription>
            </AlertDialogHeader>

            <AlertDialogFooter>
              <AlertDialogCancel>
                Cancel
              </AlertDialogCancel>

              <AlertDialogAction
                onClick={() => {
                  if (conversationToDelete) {
                    handleDeleteConversation(
                      conversationToDelete
                    )
                  }
                  setConversationToDelete(null)
                }}
                className="bg-red-600 hover:bg-red-700"
              >
                Delete
              </AlertDialogAction>
            </AlertDialogFooter>
          </AlertDialogContent>
        </AlertDialog>
    </div>
    
  )
  
}

export default ConversationSidebar