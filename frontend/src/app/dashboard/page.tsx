'use client'

/**
 * Dashboard Page
 * 
 * Main dashboard with task statistics and task list
 */

import { useEffect, useState } from 'react'
import { useTaskStore } from '@/store/taskStore'
import { Task } from '@/lib/types'
import { Plus, CheckCircle, Clock, AlertCircle, TrendingUp } from 'lucide-react'
import TaskList from '@/components/TaskList'
import TaskModal from '@/components/TaskModal'
import StatCard from '@/components/StatCard'

export default function DashboardPage() {
  const { tasks, statistics, fetchTasks, fetchStatistics } = useTaskStore()
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [selectedTask, setSelectedTask] = useState<Task | null>(null)

  useEffect(() => {
    fetchTasks()
    fetchStatistics()
  }, [fetchTasks, fetchStatistics])

  const handleEditTask = (task: Task) => {
    setSelectedTask(task)
    setIsModalOpen(true)
  }

  const handleCloseModal = () => {
    setSelectedTask(null)
    setIsModalOpen(false)
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="mt-1 text-gray-600">Manage your tasks efficiently</p>
        </div>
        <button
          onClick={() => setIsModalOpen(true)}
          className="btn btn-primary flex items-center space-x-2"
        >
          <Plus className="w-5 h-5" />
          <span>New Task</span>
        </button>
      </div>

      {/* Statistics */}
      {statistics && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <StatCard
            title="Total Tasks"
            value={statistics.total}
            icon={<TrendingUp className="w-6 h-6" />}
            color="blue"
          />
          <StatCard
            title="To Do"
            value={statistics.by_status.todo}
            icon={<Clock className="w-6 h-6" />}
            color="gray"
          />
          <StatCard
            title="In Progress"
            value={statistics.by_status.in_progress}
            icon={<AlertCircle className="w-6 h-6" />}
            color="yellow"
          />
          <StatCard
            title="Completed"
            value={statistics.by_status.done}
            icon={<CheckCircle className="w-6 h-6" />}
            color="green"
          />
        </div>
      )}

      {/* Task List */}
      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Your Tasks</h2>
        <TaskList tasks={tasks} onEdit={handleEditTask} />
      </div>

      {/* Task Modal */}
      <TaskModal
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        task={selectedTask}
      />
    </div>
  )
}
