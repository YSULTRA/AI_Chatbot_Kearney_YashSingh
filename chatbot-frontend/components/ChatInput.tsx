import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Send } from "lucide-react"

interface ChatInputProps {
  onSend: (message: string) => void
  disabled?: boolean
}

export function ChatInput({ onSend, disabled }: ChatInputProps) {
  const [message, setMessage] = useState("")
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto"
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`
    }
  }, [message])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (message.trim() && !disabled) {
      onSend(message)
      setMessage("")
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="relative">
      <div className="flex items-end gap-3 p-4 bg-gray-50 rounded-2xl border-2 border-gray-300 hover:border-purple-400 transition-colors shadow-sm">
        <textarea
          ref={textareaRef}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask me anything about your sugar commodity data..."
          disabled={disabled}
          rows={1}
          className="flex-1 resize-none bg-transparent border-0 focus:outline-none text-base py-2 px-2 max-h-32 text-gray-900 placeholder:text-gray-500 font-medium"
          style={{ color: '#1f2937' }}
        />

        <Button
          type="submit"
          disabled={disabled || !message.trim()}
          size="icon"
          className="h-11 w-11 rounded-xl bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 transition-all shadow-md disabled:opacity-50 disabled:cursor-not-allowed flex-shrink-0"
        >
          <Send className="w-5 h-5 text-white" />
        </Button>
      </div>

      <div className="flex items-center justify-between mt-2 px-2 text-xs font-medium text-gray-500">
        <span>Press Enter to send • Shift+Enter for new line</span>
      </div>
    </form>
  )
}
