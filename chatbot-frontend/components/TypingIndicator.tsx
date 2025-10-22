import { motion } from "framer-motion"

export function TypingIndicator() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="flex items-center gap-3 px-5 py-4 bg-white rounded-2xl shadow-md border-2 border-gray-200 max-w-[120px]"
    >
      <div className="flex gap-1.5">
        <div className="w-2 h-2 bg-purple-500 rounded-full typing-dot" />
        <div className="w-2 h-2 bg-purple-500 rounded-full typing-dot" />
        <div className="w-2 h-2 bg-purple-500 rounded-full typing-dot" />
      </div>
    </motion.div>
  )
}
