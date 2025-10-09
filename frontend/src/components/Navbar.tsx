'use client'

/**
 * Navigation Bar Component
 * 
 * Demonstrates component composition and user interaction
 */

import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useAuthStore } from '@/store/authStore'
import { LogOut, User, LayoutDashboard } from 'lucide-react'

export default function Navbar() {
  const router = useRouter()
  const { user, logout } = useAuthStore()

  const handleLogout = () => {
    logout()
    router.push('/')
  }

  return (
    <nav className="bg-white border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/dashboard" className="flex items-center space-x-2">
              <LayoutDashboard className="w-8 h-8 text-primary-600" />
              <span className="text-xl font-bold text-gray-900">TaskManager</span>
            </Link>
          </div>

          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2 text-gray-700">
              <User className="w-5 h-5" />
              <span>{user?.full_name || user?.email}</span>
            </div>
            <button
              onClick={handleLogout}
              className="btn btn-secondary flex items-center space-x-2"
            >
              <LogOut className="w-4 h-4" />
              <span>Logout</span>
            </button>
          </div>
        </div>
      </div>
    </nav>
  )
}
