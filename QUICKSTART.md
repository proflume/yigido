# 🚀 Quick Start Guide

Get the Task Manager application running in 5 minutes!

## Prerequisites

Choose one of these options:

**Option A: Docker (Easiest)**
- Docker Desktop installed
- That's it!

**Option B: Local Development**
- Python 3.11+
- Node.js 20+
- PostgreSQL 16+

---

## 🐳 Option A: Docker (Recommended)

### 1. Clone and Start

```bash
# Clone the repository
git clone <your-repo-url>
cd task-manager

# Copy environment files
cp backend/.env.example backend/.env
cp frontend/.env.local.example frontend/.env.local

# Build and start all services
make build
make up
```

### 2. Initialize Database

```bash
# Run migrations
make migrate

# Create admin user
make createsuperuser
```

### 3. Access Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api/v1
- **API Docs**: http://localhost:8000/api/docs
- **Admin Panel**: http://localhost:8000/admin

### Common Commands

```bash
make logs              # View all logs
make logs-backend      # View backend logs
make logs-frontend     # View frontend logs
make down              # Stop all services
make restart           # Restart services
make test-backend      # Run backend tests
make test-frontend     # Run frontend tests
```

---

## 💻 Option B: Local Development

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env and set your database credentials

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start server
python manage.py runserver
```

Backend will be available at http://localhost:8000

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Setup environment
cp .env.local.example .env.local

# Start development server
npm run dev
```

Frontend will be available at http://localhost:3000

---

## 📝 First Steps

### 1. Create Your First User

**Via Frontend:**
1. Go to http://localhost:3000
2. Click "Sign Up"
3. Fill in the registration form
4. Login with your credentials

**Via Admin:**
1. Go to http://localhost:8000/admin
2. Login with superuser credentials
3. Add users, tasks, categories

### 2. Create Your First Task

1. Login to the frontend
2. Click "New Task" button
3. Fill in task details:
   - Title: "My first task"
   - Priority: High
   - Status: To Do
4. Click "Create Task"

### 3. Explore the API

1. Go to http://localhost:8000/api/docs
2. Click "Authorize" and enter your JWT token
3. Try the different endpoints

---

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest                          # Run all tests
pytest -v                       # Verbose output
pytest --cov=apps              # With coverage
pytest tests/test_tasks.py     # Specific file
```

### Frontend Tests

```bash
cd frontend
npm test                        # Run all tests
npm test -- --coverage         # With coverage
npm test -- --watch            # Watch mode
```

---

## 🐛 Troubleshooting

### Docker Issues

**Problem:** Port already in use
```bash
# Find and kill process using port 8000
lsof -ti:8000 | xargs kill -9

# Or change port in docker-compose.yml
ports:
  - "8001:8000"  # Change 8000 to 8001
```

**Problem:** Database connection failed
```bash
# Check if database is running
docker-compose ps

# Restart database
docker-compose restart db
```

### Local Development Issues

**Problem:** Module not found (Python)
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

**Problem:** Module not found (Node)
```bash
# Clear and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Problem:** Database migration errors
```bash
# Reset database (WARNING: deletes all data)
python manage.py flush
python manage.py migrate
```

---

## 📚 Next Steps

### Learn the Codebase

1. **Start with Documentation**
   - [Software Engineering Concepts](./docs/SOFTWARE_ENGINEERING.md)
   - [System Design](./docs/SYSTEM_DESIGN.md)
   - [API Documentation](./docs/API.md)
   - [Learning Path](./docs/LEARNING_PATH.md)

2. **Explore the Code**
   - Backend: `backend/apps/`
   - Frontend: `frontend/src/`
   - Tests: `backend/tests/`, `frontend/__tests__/`

3. **Make Changes**
   - Add a new field to tasks
   - Create a new API endpoint
   - Build a new component
   - Write tests

### Deploy to Production

Follow the [Deployment Guide](./docs/DEPLOYMENT.md) to deploy to:
- AWS
- DigitalOcean
- Heroku
- Vercel

---

## 🆘 Getting Help

- **Documentation**: Check the `docs/` folder
- **Issues**: Open a GitHub issue
- **Community**: Join discussions

---

## ✅ Verification Checklist

Before moving forward, verify:

- [ ] Backend API is accessible at http://localhost:8000
- [ ] Frontend is accessible at http://localhost:3000
- [ ] Can create a user account
- [ ] Can login successfully
- [ ] Can create a task
- [ ] Can view task list
- [ ] API documentation loads
- [ ] Tests pass (optional but recommended)

---

**You're all set! Start building! 🎉**

For detailed learning, see [LEARNING_PATH.md](./docs/LEARNING_PATH.md)
