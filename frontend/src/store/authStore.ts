/**
 * Authentication Store
 * 
 * This demonstrates state management best practices with Zustand:
 * - Centralized auth state
 * - Persistent storage
 * - Type-safe actions
 */

import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { User } from '@/lib/types'
import { authAPI } from '@/lib/api'

interface AuthState {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (email: string, password: string) => Promise<void>
  register: (data: any) => Promise<void>
  logout: () => void
  fetchUser: () => Promise<void>
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      isAuthenticated: false,
      isLoading: false,

      login: async (email: string, password: string) => {
        set({ isLoading: true })
        try {
          const response = await authAPI.login(email, password)
          
          // Store tokens
          localStorage.setItem('access_token', response.access)
          localStorage.setItem('refresh_token', response.refresh)
          
          // Fetch user data
          const user = await authAPI.getProfile()
          
          set({
            user,
            isAuthenticated: true,
            isLoading: false,
          })
        } catch (error) {
          set({ isLoading: false })
          throw error
        }
      },

      register: async (data: any) => {
        set({ isLoading: true })
        try {
          await authAPI.register(data)
          
          // Auto-login after registration
          await useAuthStore.getState().login(data.email, data.password)
        } catch (error) {
          set({ isLoading: false })
          throw error
        }
      },

      logout: () => {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        set({
          user: null,
          isAuthenticated: false,
        })
      },

      fetchUser: async () => {
        try {
          const user = await authAPI.getProfile()
          set({ user, isAuthenticated: true })
        } catch (error) {
          set({ user: null, isAuthenticated: false })
        }
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
)
