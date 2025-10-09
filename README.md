# 🚀 Full-Stack Task Manager

> A comprehensive, production-ready task management application built with **Next.js 14** and **Django**, demonstrating modern software engineering best practices and system design principles.

[![CI/CD](https://github.com/yourusername/task-manager/workflows/CI%2FCD%20Pipeline/badge.svg)](https://github.com/yourusername/task-manager/actions)
[![codecov](https://codecov.io/gh/yourusername/task-manager/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/task-manager)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Learning Resources](#learning-resources)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

This project serves dual purposes:

1. **Production Application**: A fully functional task management system with authentication, CRUD operations, real-time updates, and analytics.

2. **Educational Resource**: A comprehensive guide to modern full-stack development, covering:
   - Software engineering principles (SOLID, DRY, KISS)
   - System design patterns
   - API architecture
   - Database modeling
   - Authentication & Authorization
   - Testing strategies
   - DevOps & CI/CD
   - Performance optimization
   - Security best practices

---

## ✨ Features

### 🔐 Authentication & User Management
- JWT-based authentication
- User registration and login
- Profile management
- Password change functionality
- Secure password hashing

### 📝 Task Management
- Create, read, update, delete tasks
- Task categories and priorities
- Due dates with overdue tracking
- Task status workflow (Todo → In Progress → Done)
- Rich task descriptions
- Search and filtering
- Sorting and pagination

### 📊 Analytics & Insights
- Task statistics dashboard
- Status breakdown
- Priority distribution
- Overdue task tracking
- User productivity metrics

### 💬 Collaboration
- Comments on tasks
- Task sharing (future feature)
- Activity tracking (future feature)

### 🎨 User Experience
- Responsive design (mobile, tablet, desktop)
- Modern, clean UI with Tailwind CSS
- Real-time updates
- Form validation
- Error handling
- Loading states

---

## 🛠️ Tech Stack

### Backend
- **Framework**: Django 4.2
- **API**: Django REST Framework
- **Database**: PostgreSQL 16
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Testing**: Pytest
- **Code Quality**: Black, Flake8, isort
- **Documentation**: drf-spectacular (OpenAPI/Swagger)

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **Forms**: React Hook Form + Zod
- **HTTP Client**: Axios
- **Testing**: Jest + React Testing Library

### DevOps
- **Containerization**: Docker & Docker Compose
- **Web Server**: Nginx
- **CI/CD**: GitHub Actions
- **Monitoring**: Sentry (optional)
- **Logging**: ELK Stack (optional)

---

## 🚀 Quick Start

### Prerequisites

- **Docker** and **Docker Compose** (recommended)
  OR
- **Python 3.11+**, **Node.js 20+**, **PostgreSQL 16+**

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/task-manager.git
cd task-manager

# Build and start services
make build
make up

# Run migrations
make migrate

# Create superuser
make createsuperuser

# View logs
make logs
```

**Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api/v1
- API Docs: http://localhost:8000/api/docs
- Admin: http://localhost:8000/admin

### Option 2: Local Development

**Backend:**
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Edit .env with your configuration

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

**Frontend:**
```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.local.example .env.local

# Start development server
npm run dev
```

---

## 🏗️ Architecture

### High-Level Architecture

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   Next.js   │ ──────→ │   Django    │ ──────→ │ PostgreSQL  │
│  Frontend   │ ←────── │   Backend   │ ←────── │  Database   │
└─────────────┘         └─────────────┘         └─────────────┘
      │                        │
      │                        │
      ↓                        ↓
  Tailwind CSS           Django REST Framework
  Zustand Store          JWT Authentication
  React Hook Form        Database ORM
```

### Project Structure

```
task-manager/
├── backend/                    # Django backend
│   ├── apps/                  # Django applications
│   │   ├── core/             # Core utilities
│   │   ├── users/            # User management
│   │   └── tasks/            # Task management
│   ├── config/               # Django settings
│   ├── tests/                # Backend tests
│   └── requirements.txt      # Python dependencies
│
├── frontend/                  # Next.js frontend
│   ├── src/
│   │   ├── app/             # Next.js App Router
│   │   ├── components/      # React components
│   │   ├── lib/             # Utilities & API
│   │   └── store/           # State management
│   └── package.json         # Node dependencies
│
├── docs/                      # Documentation
│   ├── SOFTWARE_ENGINEERING.md
│   ├── SYSTEM_DESIGN.md
│   ├── API.md
│   └── DEPLOYMENT.md
│
├── .github/workflows/        # CI/CD pipelines
├── docker-compose.yml        # Development compose
└── Makefile                  # Development commands
```

---

## 📚 Learning Resources

### Documentation

1. **[Software Engineering Concepts](./docs/SOFTWARE_ENGINEERING.md)**
   - SOLID Principles with examples
   - Design Patterns (Factory, Observer, Strategy, etc.)
   - Clean Architecture
   - Code Quality (DRY, KISS, YAGNI)
   - Testing Strategies

2. **[System Design](./docs/SYSTEM_DESIGN.md)**
   - Architecture patterns
   - Database design & normalization
   - RESTful API design
   - Authentication & Authorization (JWT)
   - Scalability considerations
   - Performance optimization
   - Security best practices

3. **[API Documentation](./docs/API.md)**
   - Complete API reference
   - Request/Response examples
   - Authentication flows
   - Error handling

4. **[Deployment Guide](./docs/DEPLOYMENT.md)**
   - Production checklist
   - Docker deployment
   - Cloud deployment (AWS, DigitalOcean, Heroku)
   - CI/CD pipelines
   - Monitoring & logging

### Key Concepts Demonstrated

#### Backend (Django)
- Custom User model
- ViewSets and Serializers
- JWT authentication
- Permission classes
- Query optimization (select_related, prefetch_related)
- Custom actions
- Filtering and pagination
- Admin customization

#### Frontend (Next.js)
- App Router architecture
- Server & Client Components
- TypeScript type safety
- Form handling with validation
- State management with Zustand
- API integration with Axios
- Responsive design
- Error boundaries

#### DevOps
- Docker multi-stage builds
- Docker Compose orchestration
- Nginx reverse proxy
- CI/CD with GitHub Actions
- Automated testing
- Security scanning

---

## 📖 API Documentation

### Authentication

```bash
# Register
POST /api/v1/auth/users/
{
  "email": "user@example.com",
  "password": "securepass123",
  "password_confirm": "securepass123",
  "first_name": "John",
  "last_name": "Doe"
}

# Login
POST /api/v1/auth/token/
{
  "email": "user@example.com",
  "password": "securepass123"
}
# Returns: { "access": "...", "refresh": "..." }
```

### Tasks

```bash
# List tasks
GET /api/v1/tasks/?status=in_progress&priority=high

# Create task
POST /api/v1/tasks/
{
  "title": "Complete project",
  "description": "Finish the documentation",
  "priority": "high",
  "due_date": "2024-12-31T23:59:59Z"
}

# Get statistics
GET /api/v1/tasks/statistics/
```

**Interactive API Docs**: http://localhost:8000/api/docs/

Full API documentation: [docs/API.md](./docs/API.md)

---

## 🧪 Testing

```bash
# Backend tests
make test-backend
# OR
cd backend && pytest --cov=apps

# Frontend tests
make test-frontend
# OR
cd frontend && npm test

# Lint
make lint-backend
make lint-frontend
```

---

## 🔒 Security

- JWT token-based authentication
- Password hashing with PBKDF2
- CORS configuration
- CSRF protection
- SQL injection prevention (ORM)
- XSS protection
- Security headers in production
- Input validation
- Rate limiting (production)

---

## 🚢 Deployment

### Quick Deploy with Docker

```bash
# Production deployment
docker-compose -f docker-compose.prod.yml up -d
```

### Cloud Platforms

- **AWS**: EC2 + RDS + S3
- **DigitalOcean**: App Platform
- **Heroku**: Backend + Vercel for Frontend
- **Railway**: Full-stack deployment

See [Deployment Guide](./docs/DEPLOYMENT.md) for detailed instructions.

---

## 📊 Performance

- Database query optimization with select_related/prefetch_related
- Redis caching (optional)
- CDN for static files
- Image optimization (Next.js)
- Code splitting and lazy loading
- Gzip compression
- Database indexing

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](./CONTRIBUTING.md).

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Django community for excellent framework and documentation
- Next.js team for the amazing React framework
- All open-source contributors whose libraries made this possible

---

## 📧 Contact

- **Project Link**: https://github.com/yourusername/task-manager
- **Documentation**: https://yourusername.github.io/task-manager
- **Issues**: https://github.com/yourusername/task-manager/issues

---

## 🗺️ Roadmap

- [ ] Real-time updates with WebSockets
- [ ] Team collaboration features
- [ ] File attachments
- [ ] Task templates
- [ ] Mobile app (React Native)
- [ ] Email notifications
- [ ] Calendar integration
- [ ] Advanced analytics
- [ ] Export/Import functionality
- [ ] Dark mode

---

**Built with ❤️ for learning and teaching modern full-stack development**

⭐ If you find this project helpful, please give it a star!
