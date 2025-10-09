import Link from 'next/link'
import { ArrowRight, CheckCircle, BarChart3, Users } from 'lucide-react'

export default function HomePage() {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <div className="bg-gradient-to-br from-primary-600 to-primary-800 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center">
            <h1 className="text-5xl font-bold mb-6">
              Task Management Made Simple
            </h1>
            <p className="text-xl mb-8 text-primary-100">
              A full-stack application demonstrating best practices in software engineering
            </p>
            <div className="flex gap-4 justify-center">
              <Link
                href="/login"
                className="px-8 py-3 bg-white text-primary-600 rounded-lg font-semibold hover:bg-gray-100 transition-colors inline-flex items-center gap-2"
              >
                Get Started
                <ArrowRight className="w-5 h-5" />
              </Link>
              <Link
                href="/register"
                className="px-8 py-3 bg-primary-700 text-white rounded-lg font-semibold hover:bg-primary-800 transition-colors border-2 border-white"
              >
                Sign Up
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
        <h2 className="text-3xl font-bold text-center mb-12">
          Built with Best Practices
        </h2>
        
        <div className="grid md:grid-cols-3 gap-8">
          <FeatureCard
            icon={<CheckCircle className="w-12 h-12 text-primary-600" />}
            title="Task Management"
            description="Create, organize, and track tasks with priorities, categories, and due dates."
          />
          <FeatureCard
            icon={<BarChart3 className="w-12 h-12 text-primary-600" />}
            title="Analytics"
            description="Get insights into your productivity with detailed statistics and reports."
          />
          <FeatureCard
            icon={<Users className="w-12 h-12 text-primary-600" />}
            title="Collaboration"
            description="Add comments and collaborate with team members on tasks."
          />
        </div>
      </div>

      {/* Technology Stack */}
      <div className="bg-gray-100 py-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-12">
            Technology Stack
          </h2>
          
          <div className="grid md:grid-cols-2 gap-12">
            <TechStack
              title="Frontend"
              technologies={[
                'Next.js 14 with App Router',
                'TypeScript for type safety',
                'Tailwind CSS for styling',
                'Zustand for state management',
                'React Hook Form for forms',
                'Axios for API calls',
              ]}
            />
            <TechStack
              title="Backend"
              technologies={[
                'Django 4.2 framework',
                'Django REST Framework',
                'JWT authentication',
                'PostgreSQL database',
                'Comprehensive test suite',
                'API documentation',
              ]}
            />
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p className="text-gray-400">
            A demonstration of full-stack development best practices
          </p>
          <p className="text-gray-500 mt-2">
            Built with Next.js, Django, TypeScript, and Tailwind CSS
          </p>
        </div>
      </footer>
    </div>
  )
}

function FeatureCard({ icon, title, description }: {
  icon: React.ReactNode
  title: string
  description: string
}) {
  return (
    <div className="card text-center">
      <div className="flex justify-center mb-4">{icon}</div>
      <h3 className="text-xl font-semibold mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  )
}

function TechStack({ title, technologies }: {
  title: string
  technologies: string[]
}) {
  return (
    <div className="card">
      <h3 className="text-2xl font-bold mb-4">{title}</h3>
      <ul className="space-y-3">
        {technologies.map((tech) => (
          <li key={tech} className="flex items-center gap-3">
            <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
            <span>{tech}</span>
          </li>
        ))}
      </ul>
    </div>
  )
}
