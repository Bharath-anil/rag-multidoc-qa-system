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
}

function ConversationSidebar({
  conversations,
  activeConversationId,
  onSelectConversation,
  onNewChat,
}: Props) {
  return (
    <div className="flex flex-col h-full p-3">
      <button
        onClick={onNewChat}
        className="w-full p-3 mb-4 rounded-lg bg-zinc-800 hover:bg-zinc-700"
      >
        + New Chat
      </button>

      <div className="flex flex-col gap-2 overflow-y-auto">
        {conversations.map((conversation) => (
          <button
            key={conversation.id}
            onClick={() =>
              onSelectConversation(conversation.id)
            }
            className={`w-full text-left p-3 rounded-lg transition ${
              activeConversationId === conversation.id
                ? "bg-zinc-700"
                : "hover:bg-zinc-900"
            }`}
          >
            {conversation.title}
          </button>
        ))}
      </div>
    </div>
  )
}

export default ConversationSidebar