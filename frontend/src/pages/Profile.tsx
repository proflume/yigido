import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import toast from 'react-hot-toast'
import api from '@/lib/axios'
import { useAuthStore } from '@/stores/authStore'
import { User, Save } from 'lucide-react'

interface ProfileForm {
  first_name: string
  last_name: string
  avatar_url: string
}

const Profile = () => {
  const { user, updateUser } = useAuthStore()
  const queryClient = useQueryClient()
  const [isLoading, setIsLoading] = useState(false)

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<ProfileForm>({
    defaultValues: {
      first_name: user?.first_name || '',
      last_name: user?.last_name || '',
      avatar_url: user?.avatar_url || '',
    },
  })

  const updateMutation = useMutation({
    mutationFn: (data: ProfileForm) => api.put('/users/profile', data),
    onSuccess: (response) => {
      updateUser(response.data.user)
      queryClient.invalidateQueries({ queryKey: ['current-user'] })
      toast.success('Profile updated successfully')
    },
    onError: () => {
      toast.error('Failed to update profile')
    },
  })

  const onSubmit = (data: ProfileForm) => {
    updateMutation.mutate(data)
  }

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Profile</h1>
        <p className="text-gray-600 mt-2">Manage your account settings</p>
      </div>

      <div className="max-w-2xl">
        <div className="card mb-6">
          <div className="flex items-center space-x-4 mb-6">
            <div className="w-20 h-20 bg-primary-100 rounded-full flex items-center justify-center">
              {user?.avatar_url ? (
                <img src={user.avatar_url} alt={user.username} className="w-20 h-20 rounded-full" />
              ) : (
                <User className="w-10 h-10 text-primary-600" />
              )}
            </div>
            <div>
              <h2 className="text-xl font-bold text-gray-900">{user?.username}</h2>
              <p className="text-gray-600">{user?.email}</p>
            </div>
          </div>

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  First Name
                </label>
                <input
                  {...register('first_name')}
                  type="text"
                  className="input"
                  placeholder="John"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Last Name
                </label>
                <input
                  {...register('last_name')}
                  type="text"
                  className="input"
                  placeholder="Doe"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Avatar URL
              </label>
              <input
                {...register('avatar_url')}
                type="url"
                className="input"
                placeholder="https://example.com/avatar.jpg"
              />
            </div>

            <button
              type="submit"
              disabled={updateMutation.isPending}
              className="btn-primary flex items-center space-x-2"
            >
              <Save className="w-5 h-5" />
              <span>{updateMutation.isPending ? 'Saving...' : 'Save Changes'}</span>
            </button>
          </form>
        </div>

        <div className="card border-red-200">
          <h3 className="text-lg font-bold text-red-600 mb-4">Danger Zone</h3>
          <p className="text-gray-600 mb-4">
            Once you delete your account, there is no going back. Please be certain.
          </p>
          <button className="btn-danger">
            Delete Account
          </button>
        </div>
      </div>
    </div>
  )
}

export default Profile
