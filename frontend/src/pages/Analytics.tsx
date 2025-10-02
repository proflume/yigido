import { useQuery } from '@tanstack/react-query'
import api from '@/lib/axios'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

const Analytics = () => {
  const { data: productivityData, isLoading } = useQuery({
    queryKey: ['productivity'],
    queryFn: async () => {
      const response = await api.get('/analytics/productivity')
      return response.data
    },
  })

  if (isLoading) {
    return (
      <div className="p-8">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-gray-200 rounded w-1/4"></div>
          <div className="card h-96"></div>
        </div>
      </div>
    )
  }

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Analytics</h1>
        <p className="text-gray-600 mt-2">Track your productivity and progress</p>
      </div>

      <div className="card">
        <h2 className="text-xl font-bold text-gray-900 mb-6">Tasks Completed (Last 30 Days)</h2>
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={productivityData?.daily_completed || []}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Line 
              type="monotone" 
              dataKey="count" 
              stroke="#3b82f6" 
              strokeWidth={2}
              dot={{ fill: '#3b82f6' }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}

export default Analytics
