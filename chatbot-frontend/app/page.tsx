"use client"

import { useEffect, useState, useRef } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { api } from "@/lib/api"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Card } from "@/components/ui/card"
import { ChatMessage } from "@/components/ChatMessage"
import { ChatInput } from "@/components/ChatInput"
import { TypingIndicator } from "@/components/TypingIndicator"
import { Sparkles, AlertCircle, Bot, DollarSign, Package, TrendingUp, Building2 } from "lucide-react"

interface Message {
  role: "user" | "assistant"
  content: string
  sources?: any[]
  timestamp?: string
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([])
  const [loading, setLoading] = useState(false)
  const [stats, setStats] = useState<any>(null)
  const [backendStatus, setBackendStatus] = useState<"checking" | "online" | "offline">("checking")
  const scrollRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollIntoView({ behavior: "smooth" })
    }
  }, [messages, loading])

  useEffect(() => {
    checkBackendHealth()
    fetchStats()
  }, [])

  const checkBackendHealth = async () => {
    try {
      const response = await api.get("/")
      if (response.data.status === "healthy") {
        setBackendStatus("online")
      }
    } catch (error) {
      setBackendStatus("offline")
    }
  }

  const fetchStats = async () => {
    try {
      const response = await api.get("/api/stats")
      setStats(response.data)
    } catch (error) {
      console.error("Error fetching stats:", error)
    }
  }

  const handleSend = async (message: string) => {
    if (backendStatus === "offline") {
      alert("Backend server is not running. Please start your FastAPI server.")
      return
    }

    const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    const userMessage: Message = { role: "user", content: message, timestamp }
    setMessages((prev) => [...prev, userMessage])
    setLoading(true)

    try {
      const response = await api.post("/api/chat", {
        message,
        conversation_history: messages.map((m) => ({
          role: m.role,
          content: m.content,
        })),
      })

      const assistantMessage: Message = {
        role: "assistant",
        content: response.data.answer,
        sources: response.data.sources,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      }
      setMessages((prev) => [...prev, assistantMessage])
    } catch (error) {
      console.error("Error sending message:", error)
      const errorMessage: Message = {
        role: "assistant",
        content: "Sorry, I encountered an error. Please make sure the backend server is running.",
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  const quickQuestions = [
    "Which supplier provides the cheapest sugar?",
    "What's the total spend on all commodities?",
    "List all sugars starting with 'B'",
    "Show me the most expensive commodity",
  ]

  const formatNumber = (num: number) => {
    return new Intl.NumberFormat('en-US').format(Math.round(num))
  }

  return (
    <div className="min-h-screen" style={{ background: 'linear-gradient(135deg, #f5f7fa 0%, #e9ecf5 100%)' }}>
      <div className="max-w-5xl mx-auto px-4 py-6">

        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-6"
        >
          {/* Title Row */}
          <div className="flex items-center justify-center gap-3 mb-3">
            <div className="w-12 h-12 bg-gradient-to-br from-purple-600 to-pink-600 rounded-2xl shadow-lg flex items-center justify-center">
              <Sparkles className="w-6 h-6 text-white" />
            </div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 bg-clip-text text-transparent">
              Sugar Commodity AI
            </h1>
          </div>

          {/* Status Badge - Separate Row */}
          <div className="flex justify-center mt-3">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white shadow-md border-2 border-gray-200">
              <div className={`w-2.5 h-2.5 rounded-full ${backendStatus === "online" ? "bg-green-500 animate-pulse" : "bg-red-500"}`} />
              <span className="text-sm font-semibold text-gray-800">
                {backendStatus === "online" ? "🟢 Connected" : "🔴 Disconnected"}
              </span>
            </div>
          </div>
        </motion.div>

        {/* Stats Bar - Horizontal Compact */}
        {stats && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-6"
          >
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              <Card className="p-4 bg-white shadow-md border-2 border-gray-200 hover:shadow-lg transition-shadow">
                <div className="flex items-center gap-3">
                  <div className="p-2.5 bg-emerald-100 rounded-xl">
                    <DollarSign className="w-5 h-5 text-emerald-600" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-xs font-medium text-gray-600 uppercase tracking-wide">Total Spend</p>
                    <p className="text-xl font-bold text-gray-900">${formatNumber(stats.total_spend / 1000)}K</p>
                  </div>
                </div>
              </Card>

              <Card className="p-4 bg-white shadow-md border-2 border-gray-200 hover:shadow-lg transition-shadow">
                <div className="flex items-center gap-3">
                  <div className="p-2.5 bg-blue-100 rounded-xl">
                    <Package className="w-5 h-5 text-blue-600" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-xs font-medium text-gray-600 uppercase tracking-wide">Quantity</p>
                    <p className="text-xl font-bold text-gray-900">{formatNumber(stats.total_quantity / 1000)}K kg</p>
                  </div>
                </div>
              </Card>

              <Card className="p-4 bg-white shadow-md border-2 border-gray-200 hover:shadow-lg transition-shadow">
                <div className="flex items-center gap-3">
                  <div className="p-2.5 bg-purple-100 rounded-xl">
                    <TrendingUp className="w-5 h-5 text-purple-600" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-xs font-medium text-gray-600 uppercase tracking-wide">Avg $/kg</p>
                    <p className="text-xl font-bold text-gray-900">${stats.avg_price_per_kg?.toFixed(2)}</p>
                  </div>
                </div>
              </Card>

              <Card className="p-4 bg-white shadow-md border-2 border-gray-200 hover:shadow-lg transition-shadow">
                <div className="flex items-center gap-3">
                  <div className="p-2.5 bg-orange-100 rounded-xl">
                    <Building2 className="w-5 h-5 text-orange-600" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-xs font-medium text-gray-600 uppercase tracking-wide">Suppliers</p>
                    <p className="text-xl font-bold text-gray-900">{stats.total_commodities}</p>
                  </div>
                </div>
              </Card>
            </div>
          </motion.div>
        )}

        {/* Offline Warning */}
        <AnimatePresence>
          {backendStatus === "offline" && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: "auto" }}
              exit={{ opacity: 0, height: 0 }}
              className="mb-4"
            >
              <Card className="p-4 bg-red-50 border-2 border-red-300 shadow-md">
                <div className="flex items-start gap-3">
                  <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
                  <div className="flex-1 space-y-2">
                    <p className="text-sm font-semibold text-red-900">Backend server is offline</p>
                    <code className="block text-xs p-2 bg-red-100 rounded font-mono text-red-900">
                      python -m uvicorn app.main:app --reload --port 8000
                    </code>
                  </div>
                </div>
              </Card>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Chat Container */}
        <Card className="shadow-2xl border-2 border-gray-300 overflow-hidden bg-white">
          {/* Messages */}
          <ScrollArea className="h-[500px] p-6 bg-gray-50">
            {messages.length === 0 ? (
              <div className="flex flex-col items-center justify-center h-full">
                <div className="w-20 h-20 bg-gradient-to-br from-purple-500 to-pink-600 rounded-3xl flex items-center justify-center mb-4 shadow-xl">
                  <Bot className="w-10 h-10 text-white" />
                </div>
                <h3 className="text-2xl font-bold mb-2 text-gray-900">
                  How can I help you today?
                </h3>
                <p className="text-sm text-gray-600 mb-6 text-center max-w-md">
                  Ask me about commodity data, suppliers, pricing, or spending analysis
                </p>

                {/* Quick Questions */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 w-full max-w-2xl">
                  {quickQuestions.map((question, idx) => (
                    <button
                      key={idx}
                      onClick={() => handleSend(question)}
                      disabled={loading || backendStatus === "offline"}
                      className="p-4 text-sm text-left font-medium text-gray-700 bg-white hover:bg-purple-50 rounded-xl transition-all border-2 border-gray-200 hover:border-purple-400 hover:shadow-md disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {question}
                    </button>
                  ))}
                </div>
              </div>
            ) : (
              <div>
                {messages.map((msg, idx) => (
                  <ChatMessage key={idx} {...msg} />
                ))}
                {loading && (
                  <div className="flex gap-4 mb-6">
                    <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-cyan-600 flex items-center justify-center shadow-md flex-shrink-0">
                      <Bot className="w-5 h-5 text-white" />
                    </div>
                    <TypingIndicator />
                  </div>
                )}
                <div ref={scrollRef} />
              </div>
            )}
          </ScrollArea>

          {/* Input Area */}
          <div className="p-6 border-t-2 border-gray-200 bg-white">
            <ChatInput onSend={handleSend} disabled={loading || backendStatus === "offline"} />
          </div>
        </Card>

        {/* Footer */}
        <div className="text-center mt-6 text-sm font-medium text-gray-600">
          Powered by Google Gemini AI • Next.js • FastAPI
        </div>
      </div>
    </div>
  )
}
