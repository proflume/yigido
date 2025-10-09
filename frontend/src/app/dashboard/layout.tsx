'use client'

/**
 * Dashboard Layout
 * 
 * Protected layout with authentication check
 */

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuthStore } from '@/store/authStore'
import Navbar from '@/components/Navbar'

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const router = useRouter()
  const { isAuthenticated, fetchUser } = useAuthStore()

  useEffect(() => {
    const token = localStorage.getItem('access_token')
    
    if (!token) {
      router.push('/login')
      return
    }

    if (!isAuthenticated) {
      fetchUser().catch(() => {
        router.push('/login')
      })
    }
  }, [isAuthenticated, router, fetchUser])

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>
    </div>
  )
}
