import api from "../services/api"
import { useState, useEffect } from "react"

function ChatArea() {
    const [question, setQuestion] = useState("")
    const [answer, setAnswer] = useState("")
    const [asking, setAsking] = useState(false)

    //Question function
    const handleAsk = async () => {

    if (!question) {
        alert("Enter a question")
        return
    }

        try {

            setAsking(true)

            const token = localStorage.getItem("token")

            const response = await api.post(
            "/ask",
            {
                question
            },
            {
                headers: {
                Authorization: `Bearer ${token}`
                }
            }
            )

            setAnswer(response.data.answer)

            setAsking(false)

        } catch (error) {

            console.log(error)

            setAsking(false)

            alert("Question failed")
        }
    }

  return (
    <div className="flex flex-col h-full">

      <div className="flex-1 overflow-y-auto p-6">

            {answer ? (
                <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-5 text-white whitespace-pre-wrap">
                    {answer}
                </div>
            ) : (
                <div className="h-full flex items-center justify-center text-zinc-500">
                    Ask something about your documents...
                </div>
            )}

        </div>

      <div className="border-t border-zinc-800 p-4">

        <div className="flex gap-3">

          <input
            type="text"
            placeholder="Ask a question..."
            className="flex-1 bg-zinc-900 border border-zinc-700 rounded-lg p-3 text-white outline-none"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
          />

          <button className="bg-white text-black px-5 rounded-lg font-medium" onClick={handleAsk}>
             {asking ? "Thinking..." : "Send"}
          </button>

        </div>

      </div>

    </div>
  )
}

export default ChatArea