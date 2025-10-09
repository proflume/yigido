'use client'

/**
 * Task Modal Component
 * 
 * Modal for creating and editing tasks
 */

import { useEffect, useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Task } from '@/lib/types'
import { useTaskStore } from '@/store/taskStore'
import { categoriesAPI } from '@/lib/api'
import { X } from 'lucide-react'

const taskSchema = z.object({
  title: z.string().min(1, 'Title is required'),
  description: z.string().optional(),
  status: z.enum(['todo', 'in_progress', 'done']),
  priority: z.enum(['low', 'medium', 'high', 'urgent']),
  category: z.number().nullable().optional(),
  due_date: z.string().optional(),
})

type TaskFormData = z.infer<typeof taskSchema>

interface TaskModalProps {
  isOpen: boolean
  onClose: () => void
  task?: Task | null
}

export default function TaskModal({ isOpen, onClose, task }: TaskModalProps) {
  const { createTask, updateTask } = useTaskStore()
  const [categories, setCategories] = useState<any[]>([])
  const [error, setError] = useState('')

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<TaskFormData>({
    resolver: zodResolver(taskSchema),
    defaultValues: task ? {
      title: task.title,
      description: task.description,
      status: task.status,
      priority: task.priority,
      category: task.category?.id || null,
      due_date: task.due_date ? new Date(task.due_date).toISOString().slice(0, 16) : '',
    } : {
      status: 'todo',
      priority: 'medium',
    }
  })

  useEffect(() => {
    if (isOpen) {
      fetchCategories()
      if (task) {
        reset({
          title: task.title,
          description: task.description,
          status: task.status,
          priority: task.priority,
          category: task.category?.id || null,
          due_date: task.due_date ? new Date(task.due_date).toISOString().slice(0, 16) : '',
        })
      }
    }
  }, [isOpen, task, reset])

  const fetchCategories = async () => {
    try {
      const response = await categoriesAPI.list()
      setCategories(response.results || response)
    } catch (error) {
      console.error('Failed to fetch categories:', error)
    }
  }

  const onSubmit = async (data: TaskFormData) => {
    try {
      setError('')
      if (task) {
        await updateTask(task.id, data)
      } else {
        await createTask(data)
      }
      reset()
      onClose()
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to save task')
    }
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 flex justify-between items-center">
          <h2 className="text-2xl font-bold text-gray-900">
            {task ? 'Edit Task' : 'New Task'}
          </h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="p-6 space-y-4">
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg">
              {error}
            </div>
          )}

          <div>
            <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
              Title *
            </label>
            <input
              {...register('title')}
              type="text"
              id="title"
              className="input"
              placeholder="Enter task title"
            />
            {errors.title && (
              <p className="mt-1 text-sm text-red-600">{errors.title.message}</p>
            )}
          </div>

          <div>
            <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
              Description
            </label>
            <textarea
              {...register('description')}
              id="description"
              rows={4}
              className="input"
              placeholder="Enter task description"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label htmlFor="status" className="block text-sm font-medium text-gray-700 mb-1">
                Status *
              </label>
              <select {...register('status')} id="status" className="input">
                <option value="todo">To Do</option>
                <option value="in_progress">In Progress</option>
                <option value="done">Done</option>
              </select>
            </div>

            <div>
              <label htmlFor="priority" className="block text-sm font-medium text-gray-700 mb-1">
                Priority *
              </label>
              <select {...register('priority')} id="priority" className="input">
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="urgent">Urgent</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label htmlFor="category" className="block text-sm font-medium text-gray-700 mb-1">
                Category
              </label>
              <select {...register('category', { valueAsNumber: true })} id="category" className="input">
                <option value="">None</option>
                {categories.map((cat) => (
                  <option key={cat.id} value={cat.id}>
                    {cat.name}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label htmlFor="due_date" className="block text-sm font-medium text-gray-700 mb-1">
                Due Date
              </label>
              <input
                {...register('due_date')}
                type="datetime-local"
                id="due_date"
                className="input"
              />
            </div>
          </div>

          <div className="flex justify-end gap-3 pt-4 border-t border-gray-200">
            <button
              type="button"
              onClick={onClose}
              className="btn btn-secondary"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className="btn btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isSubmitting ? 'Saving...' : task ? 'Update Task' : 'Create Task'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
