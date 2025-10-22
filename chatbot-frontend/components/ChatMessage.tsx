import { motion } from "framer-motion"
import { Card } from "@/components/ui/card"
import { Bot, User, Copy, Check } from "lucide-react"
import { useState } from "react"

interface ChatMessageProps {
  role: "user" | "assistant"
  content: string
  sources?: any[]
  timestamp?: string
}

export function ChatMessage({ role, content, sources, timestamp }: ChatMessageProps) {
  const isUser = role === "user"
  const [copied, setCopied] = useState(false)

  const handleCopy = () => {
    navigator.clipboard.writeText(content)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.2 }}
      className={`flex gap-4 mb-6 ${isUser ? "flex-row-reverse" : "flex-row"}`}
    >
      {/* Avatar */}
      <div className="flex-shrink-0">
        <div
          className={`w-10 h-10 rounded-full flex items-center justify-center shadow-md ${
            isUser
              ? "bg-gradient-to-br from-purple-500 to-pink-600"
              : "bg-gradient-to-br from-blue-500 to-cyan-600"
          }`}
        >
          {isUser ? (
            <User className="w-5 h-5 text-white" />
          ) : (
            <Bot className="w-5 h-5 text-white" />
          )}
        </div>
      </div>

      {/* Message Content */}
      <div className="flex-1 max-w-[80%]">
        <Card
          className={`p-4 shadow-md border-2 ${
            isUser
              ? "bg-gradient-to-br from-purple-500 to-pink-600 border-purple-400"
              : "bg-white border-gray-200"
          }`}
        >
          {/* Message Text with Explicit Color */}
          <div
            className={`text-sm leading-relaxed whitespace-pre-wrap font-medium ${
              isUser ? "text-white" : "text-gray-900"
            }`}
            style={isUser ? {} : { color: '#111827' }}
          >
            {content}
          </div>

          {/* Sources */}
          {sources && sources.length > 0 && (
            <div className="mt-3 pt-3 border-t border-gray-300">
              <div className="text-xs font-semibold mb-2 text-gray-700 flex items-center gap-1">
                📊 Sources ({sources.length})
              </div>
              <div className="space-y-1.5">
                {sources.slice(0, 3).map((source, idx) => (
                  <div
                    key={idx}
                    className="text-xs bg-gray-100 p-2 rounded-lg font-medium"
                    style={{ color: '#374151' }}
                  >
                    <span className="font-semibold text-gray-900">{source.commodity}</span>
                    <span className="text-gray-600"> from </span>
                    <span className="font-semibold text-gray-900">{source.supplier}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </Card>

        {/* Actions (for assistant only) */}
        {!isUser && (
          <div className="flex items-center gap-2 mt-2 px-1">
            <button
              onClick={handleCopy}
              className="flex items-center gap-1 px-2 py-1 text-xs rounded-lg bg-white hover:bg-gray-100 transition-colors border border-gray-300 font-medium"
              style={{ color: '#374151' }}
            >
              {copied ? (
                <>
                  <Check className="w-3 h-3" />
                  <span>Copied!</span>
                </>
              ) : (
                <>
                  <Copy className="w-3 h-3" />
                  <span>Copy</span>
                </>
              )}
            </button>
            {timestamp && (
              <span className="text-xs font-medium ml-auto" style={{ color: '#6b7280' }}>
                {timestamp}
              </span>
            )}
          </div>
        )}
      </div>
    </motion.div>
  )
}
