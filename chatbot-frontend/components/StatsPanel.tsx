import { Card } from "@/components/ui/card"
import { DollarSign, Package, TrendingUp, Building2 } from "lucide-react"
import { motion } from "framer-motion"

interface StatsPanelProps {
  stats: any
}

export function StatsPanel({ stats }: StatsPanelProps) {
  if (!stats) return null

  const formatNumber = (num: number) => {
    return new Intl.NumberFormat('en-US', {
      maximumFractionDigits: 1,
      minimumFractionDigits: 0
    }).format(num)
  }

  const cards = [
    {
      title: "Total Spend",
      value: `$${formatNumber(stats.total_spend / 1000)}K`,
      subtitle: `$${formatNumber(stats.total_spend)}`,
      icon: DollarSign,
      gradient: "from-emerald-500 to-teal-600",
      bg: "bg-emerald-50 dark:bg-emerald-900/20",
    },
    {
      title: "Total Quantity",
      value: `${formatNumber(stats.total_quantity / 1000)}K kg`,
      subtitle: `${formatNumber(stats.total_quantity)} kilograms`,
      icon: Package,
      gradient: "from-blue-500 to-cyan-600",
      bg: "bg-blue-50 dark:bg-blue-900/20",
    },
    {
      title: "Avg Price/kg",
      value: `$${stats.avg_price_per_kg?.toFixed(2)}`,
      subtitle: "per kilogram",
      icon: TrendingUp,
      gradient: "from-purple-500 to-pink-600",
      bg: "bg-purple-50 dark:bg-purple-900/20",
    },
    {
      title: "Unique Suppliers",
      value: stats.total_commodities,
      subtitle: "commodity types",
      icon: Building2,
      gradient: "from-orange-500 to-red-600",
      bg: "bg-orange-50 dark:bg-orange-900/20",
    },
  ]

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
      {cards.map((card, index) => (
        <motion.div
          key={card.title}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.1, duration: 0.3 }}
        >
          <Card className="relative overflow-hidden group hover:shadow-xl transition-all duration-300 cursor-pointer border-2 border-gray-100 dark:border-gray-800">
            <div className="p-5">
              <div className="flex items-start justify-between mb-3">
                <div className={`p-2.5 rounded-xl ${card.bg} group-hover:scale-110 transition-transform duration-300`}>
                  <card.icon className={`w-5 h-5 bg-gradient-to-br ${card.gradient} bg-clip-text text-transparent`}
                    style={{ WebkitTextFillColor: 'transparent', WebkitBackgroundClip: 'text' }}
                  />
                </div>
              </div>

              <div className="space-y-1">
                <p className="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide">
                  {card.title}
                </p>
                <p className={`text-2xl font-bold bg-gradient-to-r ${card.gradient} bg-clip-text text-transparent`}>
                  {card.value}
                </p>
                <p className="text-xs text-gray-400 dark:text-gray-500">
                  {card.subtitle}
                </p>
              </div>
            </div>

            {/* Hover effect gradient */}
            <div className={`absolute inset-0 bg-gradient-to-r ${card.gradient} opacity-0 group-hover:opacity-5 transition-opacity duration-300`} />
          </Card>
        </motion.div>
      ))}
    </div>
  )
}
