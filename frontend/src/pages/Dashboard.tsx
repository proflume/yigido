import { useQuery } from '@tanstack/react-query'
import api from '@/lib/axios'
import { CheckCircle, Clock, AlertCircle, TrendingUp } from 'lucide-react'

const Dashboard = () => {
  const { data: stats, isLoading } = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: async () => {
      const response = await api.get('/analytics/dashboard')
      return response.data
    },
  })

  if (isLoading) {
    return (
      <div className="p-8">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-gray-200 rounded w-1/4"></div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="card h-32"></div>
            ))}
          </div>
        </div>
      </div>
    )
  }

  const statCards = [
    {
      title: 'Total Tasks',
      value: stats?.total_tasks || 0,
      icon: CheckCircle,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50',
    },
    {
      title: 'Completed This Week',
      value: stats?.completed_this_week || 0,
      icon: TrendingUp,
      color: 'text-green-600',
      bgColor: 'bg-green-50',
    },
    {
      title: 'In Progress',
      value: stats?.status_distribution?.in_progress || 0,
      icon: Clock,
      color: 'text-yellow-600',
      bgColor: 'bg-yellow-50',
    },
    {
      title: 'Overdue',
      value: stats?.overdue_tasks || 0,
      icon: AlertCircle,
      color: 'text-red-600',
      bgColor: 'bg-red-50',
    },
  ]

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-2">Overview of your tasks and productivity</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {statCards.map((card) => (
          <div key={card.title} className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">{card.title}</p>
                <p className="text-3xl font-bold text-gray-900">{card.value}</p>
              </div>
              <div className={`p-3 rounded-lg ${card.bgColor}`}>
                <card.icon className={`w-6 h-6 ${card.color}`} />
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Status Distribution</h2>
          <div className="space-y-3">
            {Object.entries(stats?.status_distribution || {}).map(([status, count]) => (
              <div key={status} className="flex items-center justify-between">
                <span className="text-gray-700 capitalize">{status.replace('_', ' ')}</span>
                <span className="font-semibold text-gray-900">{count as number}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="card">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Priority Distribution</h2>
          <div className="space-y-3">
            {Object.entries(stats?.priority_distribution || {}).map(([priority, count]) => (
              <div key={priority} className="flex items-center justify-between">
                <span className="text-gray-700 capitalize">{priority}</span>
                <span className="font-semibold text-gray-900">{count as number}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
