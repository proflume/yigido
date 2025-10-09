/**
 * TypeScript Type Definitions
 * 
 * This demonstrates type safety best practices:
 * - Shared types between frontend components
 * - API response types
 * - Form data types
 */

export interface User {
  id: number
  email: string
  first_name: string
  last_name: string
  full_name: string
  bio: string
  avatar: string | null
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface Task {
  id: number
  title: string
  description: string
  status: 'todo' | 'in_progress' | 'done'
  priority: 'low' | 'medium' | 'high' | 'urgent'
  user: User
  category: Category | null
  category_name?: string
  due_date: string | null
  completed_at: string | null
  is_overdue: boolean
  comments?: Comment[]
  created_at: string
  updated_at: string
}

export interface Category {
  id: number
  name: string
  description: string
  color: string
  task_count?: number
  created_at: string
  updated_at: string
}

export interface Comment {
  id: number
  task: number
  user: User
  text: string
  created_at: string
  updated_at: string
}

export interface TaskStatistics {
  total: number
  by_status: {
    todo: number
    in_progress: number
    done: number
  }
  by_priority: {
    low: number
    medium: number
    high: number
    urgent: number
  }
  overdue: number
}

export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterData {
  email: string
  password: string
  password_confirm: string
  first_name: string
  last_name: string
}

export interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}
