/**
 * Utility Functions
 * 
 * Reusable utility functions for the application
 */

import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'
import { format, formatDistanceToNow } from 'date-fns'

/**
 * Merge Tailwind classes
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

/**
 * Format date to readable string
 */
export function formatDate(date: string | Date): string {
  if (!date) return ''
  return format(new Date(date), 'MMM d, yyyy')
}

/**
 * Format date with time
 */
export function formatDateTime(date: string | Date): string {
  if (!date) return ''
  return format(new Date(date), 'MMM d, yyyy h:mm a')
}

/**
 * Format relative time (e.g., "2 hours ago")
 */
export function formatRelativeTime(date: string | Date): string {
  if (!date) return ''
  return formatDistanceToNow(new Date(date), { addSuffix: true })
}

/**
 * Get priority color
 */
export function getPriorityColor(priority: string): string {
  const colors: Record<string, string> = {
    low: 'text-gray-600 bg-gray-100',
    medium: 'text-blue-600 bg-blue-100',
    high: 'text-orange-600 bg-orange-100',
    urgent: 'text-red-600 bg-red-100',
  }
  return colors[priority] || colors.medium
}

/**
 * Get status color
 */
export function getStatusColor(status: string): string {
  const colors: Record<string, string> = {
    todo: 'text-gray-600 bg-gray-100',
    in_progress: 'text-blue-600 bg-blue-100',
    done: 'text-green-600 bg-green-100',
  }
  return colors[status] || colors.todo
}

/**
 * Format status text
 */
export function formatStatus(status: string): string {
  const statusMap: Record<string, string> = {
    todo: 'To Do',
    in_progress: 'In Progress',
    done: 'Done',
  }
  return statusMap[status] || status
}
