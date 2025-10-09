# Task Manager - Full Stack Application

## 📚 Educational Full-Stack Project

This is a comprehensive full-stack web application built to demonstrate **best practices in software engineering and system design**. It serves as both a functional task management system and an educational resource for learning modern web development.

## 🎯 Learning Objectives

This project teaches you:

1. **Software Engineering Principles**
   - SOLID principles
   - Clean architecture
   - Design patterns
   - Code organization
   - Testing strategies

2. **System Design Concepts**
   - Client-server architecture
   - RESTful API design
   - Database modeling
   - Authentication & Authorization
   - State management
   - Caching strategies

3. **Modern Technologies**
   - Backend: Django & Django REST Framework
   - Frontend: Next.js 14 (App Router) with TypeScript
   - Database: PostgreSQL
   - Containerization: Docker & Docker Compose
   - Testing: Pytest & Jest

## 📂 Project Structure

```
task-manager/
├── backend/                 # Django backend
│   ├── apps/               # Django applications
│   │   ├── users/         # User management
│   │   ├── tasks/         # Task management
│   │   └── core/          # Core utilities
│   ├── config/            # Django configuration
│   ├── tests/             # Backend tests
│   └── requirements.txt   # Python dependencies
│
├── frontend/              # Next.js frontend
│   ├── src/
│   │   ├── app/          # Next.js App Router pages
│   │   ├── components/   # React components
│   │   ├── lib/          # Utilities & API client
│   │   └── store/        # State management (Zustand)
│   └── package.json      # Node dependencies
│
├── docs/                 # Documentation
│   ├── SOFTWARE_ENGINEERING.md
│   ├── SYSTEM_DESIGN.md
│   ├── API.md
│   └── DEPLOYMENT.md
│
├── docker-compose.yml    # Container orchestration
└── Makefile             # Development commands
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- OR: Python 3.11+, Node.js 20+, PostgreSQL 16+

### Method 1: Docker (Recommended)

```bash
# Build and start all services
make build
make up

# Run migrations
make migrate

# Create a superuser
make createsuperuser

# View logs
make logs
```

Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api/v1
- API Docs: http://localhost:8000/api/docs
- Admin Panel: http://localhost:8000/admin

### Method 2: Local Development

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

**Frontend:**
```bash
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```

## 🧪 Testing

```bash
# Backend tests
make test-backend
# OR
cd backend && pytest

# Frontend tests
make test-frontend
# OR
cd frontend && npm test
```

## 📖 Documentation Index

1. **[Software Engineering Concepts](./SOFTWARE_ENGINEERING.md)**
   - SOLID Principles
   - Design Patterns
   - Clean Architecture
   - Testing Strategies
   - Code Quality

2. **[System Design](./SYSTEM_DESIGN.md)**
   - Architecture Overview
   - Database Design
   - API Design
   - Authentication Flow
   - Scalability Considerations

3. **[API Documentation](./API.md)**
   - Authentication Endpoints
   - Task Management Endpoints
   - Request/Response Examples

4. **[Deployment Guide](./DEPLOYMENT.md)**
   - Production Setup
   - CI/CD Pipeline
   - Monitoring & Logging
   - Security Best Practices

## 🏗️ Architecture Overview

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   Next.js   │ ──HTTP─→│   Django    │ ─────→  │ PostgreSQL  │
│  Frontend   │ ←─JSON──│   Backend   │ ←─────  │  Database   │
└─────────────┘         └─────────────┘         └─────────────┘
      │                        │
      │                        │
      ↓                        ↓
  Tailwind CSS           Django REST Framework
  Zustand Store          JWT Authentication
  React Hook Form        Database ORM
```

## 🎓 Key Learning Topics

### Backend Development

1. **Django Framework**
   - Project structure and apps
   - Models and ORM
   - Views and ViewSets
   - URL routing
   - Admin interface

2. **Django REST Framework**
   - Serializers
   - ViewSets and Actions
   - Authentication (JWT)
   - Permissions
   - Filtering and Pagination

3. **Database Design**
   - Relational modeling
   - Indexes and optimization
   - Migrations
   - Relationships (ForeignKey, ManyToMany)

### Frontend Development

1. **Next.js 14**
   - App Router
   - Server & Client Components
   - Routing and Navigation
   - API Routes
   - Metadata and SEO

2. **React Best Practices**
   - Hooks (useState, useEffect)
   - Component composition
   - Form handling (React Hook Form)
   - State management (Zustand)

3. **TypeScript**
   - Type safety
   - Interfaces and Types
   - Generics
   - Type inference

### DevOps & Deployment

1. **Docker**
   - Containerization
   - Multi-stage builds
   - Docker Compose
   - Volume management

2. **CI/CD**
   - Automated testing
   - Continuous integration
   - Deployment automation

## 🔐 Security Features

- JWT-based authentication
- Password hashing (Django's built-in)
- CORS configuration
- CSRF protection
- SQL injection prevention (ORM)
- XSS protection
- Secure headers in production

## 📊 Features

- ✅ User registration and authentication
- ✅ Task CRUD operations
- ✅ Task categorization and priorities
- ✅ Due dates and overdue tracking
- ✅ Task statistics and analytics
- ✅ Comments on tasks
- ✅ Responsive design
- ✅ Form validation
- ✅ Error handling
- ✅ API documentation

## 🤝 Contributing

This is an educational project. Feel free to:
- Study the code
- Experiment with features
- Extend functionality
- Improve documentation

## 📝 License

MIT License - See LICENSE file for details

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Docker Documentation](https://docs.docker.com/)

---

**Built with ❤️ for learning and teaching software engineering**
