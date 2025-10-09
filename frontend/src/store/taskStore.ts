/**
 * Task Store
 * 
 * State management for tasks
 */

import { create } from 'zustand'
import { Task, TaskStatistics } from '@/lib/types'
import { tasksAPI } from '@/lib/api'

interface TaskState {
  tasks: Task[]
  selectedTask: Task | null
  statistics: TaskStatistics | null
  isLoading: boolean
  fetchTasks: (params?: any) => Promise<void>
  fetchTask: (id: number) => Promise<void>
  createTask: (data: any) => Promise<void>
  updateTask: (id: number, data: any) => Promise<void>
  deleteTask: (id: number) => Promise<void>
  fetchStatistics: () => Promise<void>
}

export const useTaskStore = create<TaskState>((set, get) => ({
  tasks: [],
  selectedTask: null,
  statistics: null,
  isLoading: false,

  fetchTasks: async (params?: any) => {
    set({ isLoading: true })
    try {
      const response = await tasksAPI.list(params)
      set({ tasks: response.results || response, isLoading: false })
    } catch (error) {
      set({ isLoading: false })
      throw error
    }
  },

  fetchTask: async (id: number) => {
    set({ isLoading: true })
    try {
      const task = await tasksAPI.get(id)
      set({ selectedTask: task, isLoading: false })
    } catch (error) {
      set({ isLoading: false })
      throw error
    }
  },

  createTask: async (data: any) => {
    set({ isLoading: true })
    try {
      await tasksAPI.create(data)
      await get().fetchTasks()
    } catch (error) {
      set({ isLoading: false })
      throw error
    }
  },

  updateTask: async (id: number, data: any) => {
    set({ isLoading: true })
    try {
      await tasksAPI.update(id, data)
      await get().fetchTasks()
    } catch (error) {
      set({ isLoading: false })
      throw error
    }
  },

  deleteTask: async (id: number) => {
    set({ isLoading: true })
    try {
      await tasksAPI.delete(id)
      await get().fetchTasks()
    } catch (error) {
      set({ isLoading: false })
      throw error
    }
  },

  fetchStatistics: async () => {
    try {
      const statistics = await tasksAPI.statistics()
      set({ statistics })
    } catch (error) {
      throw error
    }
  },
}))
