# TaskFlow - Full Stack Task Management Application

A modern, full-featured task management application built with Python Flask backend and React TypeScript frontend.

## 🚀 Features

### Backend (Python/Flask)
- **RESTful API** with comprehensive endpoints
- **JWT Authentication** with access and refresh tokens
- **PostgreSQL Database** with SQLAlchemy ORM
- **Redis Caching** for performance optimization
- **WebSocket Support** for real-time updates via Socket.IO
- **Database Migrations** with Alembic
- **Input Validation** and error handling
- **Comprehensive Testing** with pytest
- **Security Best Practices** (password hashing, CORS, etc.)

### Frontend (React/TypeScript)
- **Modern React 18** with TypeScript
- **Tailwind CSS** for beautiful, responsive UI
- **React Query** for efficient data fetching and caching
- **Zustand** for state management
- **React Router** for navigation
- **React Hook Form + Zod** for form validation
- **Socket.IO Client** for real-time features
- **Recharts** for data visualization
- **Hot Toast** for notifications

### Key Capabilities
- User authentication and authorization
- Task CRUD operations with filtering and search
- Task prioritization and status tracking
- Tag-based categorization
- Real-time task updates
- Analytics dashboard with productivity metrics
- User profile management
- Responsive design for all devices

## 📋 Prerequisites

- Python 3.11+
- Node.js 20+
- PostgreSQL 16+
- Redis 7+
- Docker & Docker Compose (optional)

## 🛠️ Installation

### Using Docker (Recommended)

1. **Clone the repository**
```bash
git clone <repository-url>
cd workspace
```

2. **Create environment files**
```bash
# Backend
cp backend/.env.example backend/.env

# Frontend
cp frontend/.env.example frontend/.env
```

3. **Start all services**
```bash
docker-compose up -d
```

4. **Run database migrations**
```bash
docker-compose exec backend flask db upgrade
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000
- API Documentation: http://localhost:5000/api

### Manual Installation

#### Backend Setup

1. **Navigate to backend directory**
```bash
cd backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Initialize database**
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

6. **Run the backend**
```bash
python wsgi.py
```

#### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Run the frontend**
```bash
npm run dev
```

## 📚 API Documentation

### Authentication Endpoints

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "SecurePass123",
  "first_name": "John",
  "last_name": "Doe"
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "johndoe",
  "password": "SecurePass123"
}
```

#### Refresh Token
```http
POST /api/auth/refresh
Authorization: Bearer <refresh_token>
```

#### Get Current User
```http
GET /api/auth/me
Authorization: Bearer <access_token>
```

### Task Endpoints

#### Get All Tasks
```http
GET /api/tasks?page=1&per_page=20&status=pending&priority=high&search=query
Authorization: Bearer <access_token>
```

#### Create Task
```http
POST /api/tasks
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Complete project",
  "description": "Finish the full stack application",
  "status": "in_progress",
  "priority": "high",
  "due_date": "2024-12-31T23:59:59Z",
  "tags": ["work", "important"]
}
```

#### Update Task
```http
PUT /api/tasks/{task_id}
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Updated task title",
  "status": "completed"
}
```

#### Delete Task
```http
DELETE /api/tasks/{task_id}
Authorization: Bearer <access_token>
```

### Analytics Endpoints

#### Dashboard Statistics
```http
GET /api/analytics/dashboard
Authorization: Bearer <access_token>
```

#### Productivity Metrics
```http
GET /api/analytics/productivity
Authorization: Bearer <access_token>
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
pytest --cov=app tests/  # With coverage
```

### Frontend Tests
```bash
cd frontend
npm test
npm run test:coverage  # With coverage
```

## 🏗️ Project Structure

```
workspace/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # Flask app factory
│   │   ├── models/              # Database models
│   │   │   ├── user.py
│   │   │   └── task.py
│   │   ├── routes/              # API endpoints
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── tasks.py
│   │   │   └── analytics.py
│   │   └── utils/               # Utilities
│   │       ├── validators.py
│   │       └── error_handlers.py
│   ├── tests/                   # Test suite
│   ├── migrations/              # Database migrations
│   ├── wsgi.py                  # Application entry point
│   ├── requirements.txt         # Python dependencies
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   │   ├── Layout.tsx
│   │   │   └── TaskModal.tsx
│   │   ├── pages/               # Page components
│   │   │   ├── Login.tsx
│   │   │   ├── Register.tsx
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Tasks.tsx
│   │   │   ├── Analytics.tsx
│   │   │   └── Profile.tsx
│   │   ├── stores/              # State management
│   │   │   └── authStore.ts
│   │   ├── lib/                 # Utilities
│   │   │   ├── axios.ts
│   │   │   ├── socket.ts
│   │   │   └── utils.ts
│   │   ├── App.tsx              # Main app component
│   │   ├── main.tsx             # Entry point
│   │   └── index.css            # Global styles
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   ├── vite.config.ts
│   └── Dockerfile
├── docker-compose.yml           # Docker orchestration
└── README.md
```

## 🔧 Configuration

### Backend Environment Variables

```env
FLASK_APP=wsgi.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/fullstack_app
REDIS_URL=redis://localhost:6379/0
UPLOAD_FOLDER=/tmp/uploads
```

### Frontend Environment Variables

```env
VITE_API_URL=http://localhost:5000/api
VITE_SOCKET_URL=http://localhost:5000
```

## 🚢 Deployment

### Production Deployment Steps

1. **Update environment variables** for production
   - Set strong SECRET_KEY and JWT_SECRET_KEY
   - Update database and Redis URLs
   - Set FLASK_ENV=production

2. **Build frontend for production**
```bash
cd frontend
npm run build
```

3. **Use production-ready WSGI server**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
```

4. **Set up reverse proxy** (nginx)
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
    }

    location /api {
        proxy_pass http://localhost:5000;
    }

    location /socket.io {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

5. **Enable HTTPS** with Let's Encrypt
```bash
certbot --nginx -d your-domain.com
```

## 🔒 Security Features

- Password hashing with Werkzeug
- JWT-based authentication
- Token refresh mechanism
- Token blacklisting on logout
- CORS configuration
- SQL injection prevention via ORM
- Input validation
- Rate limiting (recommended to add)
- HTTPS in production

## 📊 Performance Optimizations

- Redis caching for analytics
- Database query optimization with indexes
- React Query for client-side caching
- Lazy loading and code splitting
- Connection pooling for database
- Pagination for large datasets

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 👥 Authors

- Your Name - Initial work

## 🙏 Acknowledgments

- Flask documentation
- React documentation
- Tailwind CSS
- All open-source contributors

## 📞 Support

For support, email support@example.com or open an issue in the repository.

---

**Built with ❤️ using Python, Flask, React, and TypeScript**
