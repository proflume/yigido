'use client'

/**
 * Task List Component
 * 
 * Displays a list of tasks with filtering and actions
 */

import { useState } from 'react'
import { Task } from '@/lib/types'
import { useTaskStore } from '@/store/taskStore'
import { 
  Edit2, 
  Trash2, 
  Calendar, 
  AlertCircle,
  ChevronDown 
} from 'lucide-react'
import { 
  formatDate, 
  getPriorityColor, 
  getStatusColor, 
  formatStatus 
} from '@/lib/utils'

interface TaskListProps {
  tasks: Task[]
  onEdit: (task: Task) => void
}

export default function TaskList({ tasks, onEdit }: TaskListProps) {
  const { deleteTask } = useTaskStore()
  const [filter, setFilter] = useState<string>('all')
  const [expandedTask, setExpandedTask] = useState<number | null>(null)

  const filteredTasks = tasks.filter(task => {
    if (filter === 'all') return true
    return task.status === filter
  })

  const handleDelete = async (id: number) => {
    if (confirm('Are you sure you want to delete this task?')) {
      try {
        await deleteTask(id)
      } catch (error) {
        alert('Failed to delete task')
      }
    }
  }

  if (tasks.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        <p>No tasks yet. Create your first task to get started!</p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {/* Filter */}
      <div className="flex gap-2">
        {['all', 'todo', 'in_progress', 'done'].map((status) => (
          <button
            key={status}
            onClick={() => setFilter(status)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              filter === status
                ? 'bg-primary-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            {status === 'all' ? 'All' : formatStatus(status)}
          </button>
        ))}
      </div>

      {/* Task Items */}
      <div className="space-y-3">
        {filteredTasks.map((task) => (
          <div
            key={task.id}
            className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
          >
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-2">
                  <h3 className="text-lg font-semibold text-gray-900">
                    {task.title}
                  </h3>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(task.status)}`}>
                    {formatStatus(task.status)}
                  </span>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getPriorityColor(task.priority)}`}>
                    {task.priority.toUpperCase()}
                  </span>
                </div>

                {task.description && (
                  <p className="text-gray-600 text-sm mb-2">
                    {expandedTask === task.id 
                      ? task.description 
                      : task.description.slice(0, 100) + (task.description.length > 100 ? '...' : '')}
                  </p>
                )}

                {task.description && task.description.length > 100 && (
                  <button
                    onClick={() => setExpandedTask(expandedTask === task.id ? null : task.id)}
                    className="text-primary-600 text-sm flex items-center gap-1"
                  >
                    {expandedTask === task.id ? 'Show less' : 'Show more'}
                    <ChevronDown className={`w-4 h-4 transition-transform ${expandedTask === task.id ? 'rotate-180' : ''}`} />
                  </button>
                )}

                <div className="flex items-center gap-4 mt-2 text-sm text-gray-500">
                  {task.category_name && (
                    <span className="flex items-center gap-1">
                      <span className="w-2 h-2 rounded-full bg-primary-500"></span>
                      {task.category_name}
                    </span>
                  )}
                  {task.due_date && (
                    <span className="flex items-center gap-1">
                      <Calendar className="w-4 h-4" />
                      {formatDate(task.due_date)}
                    </span>
                  )}
                  {task.is_overdue && (
                    <span className="flex items-center gap-1 text-red-600">
                      <AlertCircle className="w-4 h-4" />
                      Overdue
                    </span>
                  )}
                </div>
              </div>

              <div className="flex items-center gap-2 ml-4">
                <button
                  onClick={() => onEdit(task)}
                  className="p-2 text-primary-600 hover:bg-primary-50 rounded-lg transition-colors"
                  title="Edit task"
                >
                  <Edit2 className="w-5 h-5" />
                </button>
                <button
                  onClick={() => handleDelete(task.id)}
                  className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                  title="Delete task"
                >
                  <Trash2 className="w-5 h-5" />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
