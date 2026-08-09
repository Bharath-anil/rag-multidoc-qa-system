import api from "../services/api"
import { useState,useEffect, useRef  } from "react"
import ReactMarkdown from "react-markdown"
import { toast } from "sonner"
import { FileSearch ,FileText, Upload ,Search,MessageSquare } from "lucide-react";

 type Message = {
          role: "user" | "assistant"
          content: string
          sources?: string[]
        }
        
interface ChatAreaProps {
  messages: Message[]
  setMessages: React.Dispatch<
    React.SetStateAction<Message[]>
  >
  activeConversationId: string | null
}

function ChatArea({
    messages,
    setMessages,
    activeConversationId,
  }: ChatAreaProps) {
    const messagesEndRef = useRef<HTMLDivElement | null>(null)
    const [question, setQuestion] = useState("")
   
    const [asking, setAsking] = useState(false)
      
        
    useEffect(() => {
      messagesEndRef.current?.scrollIntoView({
        behavior: "smooth",
      })
    }, [messages])


    //Question function
    const handleAsk = async () => {
    
    if (!activeConversationId) {
      toast.info(
        "Create or select a chat first",
        { position: "top-right" }
      )
      return
    }
        

    if (!question.trim()) {
        toast.info("Enter a question", { position: "top-right" })
        return
    }
    const currentQuestion = question

      setMessages((prev) => [
        ...prev,
        {
          role: "user",
          content: currentQuestion,
        },
      ])

      setQuestion("")
      setAsking(true)

      try {


        const response = await api.post("/ask", {
          conversation_id: activeConversationId,
          question: currentQuestion,
          document_ids: [],
        })

        setMessages((prev) => [
          ...prev,
          {
            role: "assistant",
            content: response.data.answer,
            sources: response.data.sources || [],
          },
        ])

        setAsking(false)

      } catch (error) {

        console.log(error)

        setAsking(false)

        toast.error("Question failed", { position: "top-right" })
      }
    }

  return (
    <div className="flex flex-col h-full">

      <div className="flex-1 overflow-y-auto p-6">

            {messages.length === 0 ? (

  <div className="h-full flex flex-col items-center justify-center text-center px-6">

    <FileSearch
      size={56}
      className="text-emerald-400 mb-6"
    />

    <h2 className="text-2xl font-semibold text-white">
      Welcome to DocuMind
    </h2>

    <p className="mt-3 max-w-md text-zinc-400">
      Upload one or more PDF documents and explore them using AI-powered semantic search.
    </p>

    <div className="mt-8 w-full max-w-md space-y-3">

      <div className="flex items-center gap-3 rounded-lg border border-zinc-800 bg-zinc-900 px-4 py-3">
        <Upload size={18} className="text-emerald-400 shrink-0" />
        <span className="text-sm text-zinc-300">
          Upload PDF documents
        </span>
      </div>

      <div className="flex items-center gap-3 rounded-lg border border-zinc-800 bg-zinc-900 px-4 py-3">
        <Search size={18} className="text-emerald-400 shrink-0" />
        <span className="text-sm text-zinc-300">
          Search using semantic retrieval
        </span>
      </div>

      <div className="flex items-center gap-3 rounded-lg border border-zinc-800 bg-zinc-900 px-4 py-3">
        <MessageSquare size={18} className="text-emerald-400 shrink-0" />
        <span className="text-sm text-zinc-300">
          Ask questions about your documents
        </span>
      </div>

      <div className="flex items-center gap-3 rounded-lg border border-zinc-800 bg-zinc-900 px-4 py-3">
        <FileText size={18} className="text-emerald-400 shrink-0" />
        <span className="text-sm text-zinc-300">
          Get answers with source references
        </span>
      </div>

    </div>

  </div>

  ) : (

    <div className="space-y-4">

      {messages.map((message, index) => (

        <div
          key={index}
          className={`flex ${
            message.role === "user"
              ? "justify-end"
              : "justify-start"
          }`}
        >

          <div
            className={`max-w-[80%] rounded-xl p-4 whitespace-pre-wrap ${
              message.role === "user"
                ? "bg-white text-black"
                : "bg-zinc-900 border border-zinc-800 text-white"
            }`}
          >
            {message.role === "assistant" && (
              <div className="flex items-center gap-2 mb-3 pb-2 border-b border-zinc-800">
                <FileSearch
                  size={20} 
                  className="text-emerald-400"
                />

                <span className="font-semibold text-zinc-200">
                  Doc Assistant
                </span>
              </div>
            )}
            
           <div className="prose prose-invert max-w-none">
                <ReactMarkdown>
                    {message.content}
                </ReactMarkdown>
            </div>

            {message.role === "assistant" &&
                message.sources &&
                message.sources.length > 0 && (
                  <div className="mt-4 border-t border-zinc-700 pt-3">
                    <p className="text-xs font-medium uppercase tracking-wide text-zinc-500 mb-2">
                      Sources
                    </p>

                    <div className="flex flex-wrap gap-2">
                      {message.sources.map((source) => (
                        <span
                          key={source}
                          className="bg-zinc-800 text-xs px-2 py-1 rounded"
                        >
                         <FileText size={12} />
                          {source}
                        </span>
                      ))}
                    </div>
                  </div>
              )}

          </div>

        </div>

      ))}

      {asking && (
        <div className="flex justify-start">

          <div className="bg-zinc-900 border border-zinc-800 text-zinc-400 rounded-xl p-4">
            Thinking...
          </div>

        </div>
      )}

      <div ref={messagesEndRef}></div>

    </div>

  )}

        </div>

      <div className="border-t border-zinc-800 p-4">

        {!activeConversationId ? (

          <div className="text-center text-zinc-500 text-sm">
            Create or select a chat to start asking questions.
          </div>

        ) : (

          <div className="flex gap-3">

            <input
              type="text"
              disabled={asking}
              placeholder="Ask a question..."
              className="flex-1 bg-zinc-900 border border-zinc-700 rounded-lg p-3 text-white outline-none"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
            />

            <button
              className="bg-white text-black px-5 rounded-lg font-medium"
              onClick={handleAsk}
              disabled={asking}
            >
              {asking ? "Thinking..." : "Send"}
            </button>

          </div>

        )}

      </div>

    </div>
  )
}

export default ChatArea