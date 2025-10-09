# Best Practices Guide

A comprehensive guide to the best practices demonstrated in this project.

## Table of Contents

1. [Code Organization](#code-organization)
2. [Django Best Practices](#django-best-practices)
3. [React/Next.js Best Practices](#reactnextjs-best-practices)
4. [API Design Best Practices](#api-design-best-practices)
5. [Database Best Practices](#database-best-practices)
6. [Security Best Practices](#security-best-practices)
7. [Testing Best Practices](#testing-best-practices)
8. [Performance Best Practices](#performance-best-practices)
9. [DevOps Best Practices](#devops-best-practices)

---

## Code Organization

### Project Structure

**✅ Good:**
```
backend/
├── apps/              # Feature-based organization
│   ├── users/        # Self-contained app
│   └── tasks/        # Self-contained app
├── config/           # Project configuration
└── tests/            # Centralized tests
```

**❌ Bad:**
```
backend/
├── models.py         # All models in one file
├── views.py          # All views in one file
└── utils.py          # Misc functions
```

### File Naming

**✅ Good:**
- `user_serializer.py` (descriptive, snake_case)
- `TaskViewSet` (PascalCase for classes)
- `get_user_tasks()` (snake_case for functions)

**❌ Bad:**
- `utils.py` (too generic)
- `stuff.py` (unclear purpose)
- `getData()` (camelCase in Python)

---

## Django Best Practices

### 1. Models

**✅ Good:**
```python
class Task(models.Model):
    """
    Task model with proper documentation.
    
    Demonstrates:
    - Clear field names
    - Appropriate field types
    - Proper relationships
    - Meta options
    """
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
        ]
    
    def __str__(self):
        return self.title
```

**❌ Bad:**
```python
class Task(models.Model):
    t = models.CharField(max_length=255)  # Unclear name
    u = models.ForeignKey(User)  # No on_delete, no related_name
    # No Meta options, no __str__
```

### 2. Serializers

**✅ Good:**
```python
class TaskSerializer(serializers.ModelSerializer):
    """Separate serializers for different use cases."""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class TaskCreateSerializer(serializers.ModelSerializer):
    """Lightweight serializer for creation."""
    class Meta:
        model = Task
        fields = ('title', 'description', 'priority')
```

**❌ Bad:**
```python
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'  # Exposes everything
        # No validation, no separation of concerns
```

### 3. Views

**✅ Good:**
```python
class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet with:
    - Query optimization
    - Permission classes
    - Custom actions
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Task.objects.filter(
            user=self.request.user
        ).select_related('user', 'category')
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        # Custom action
        pass
```

**❌ Bad:**
```python
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()  # No filtering!
    serializer_class = TaskSerializer
    # No permissions, no optimization
```

### 4. Settings

**✅ Good:**
```python
# Use environment variables
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)

# Separate settings for different environments
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
```

**❌ Bad:**
```python
# Hardcoded secrets
SECRET_KEY = 'my-secret-key-123'
DEBUG = True

# No environment-specific settings
```

---

## React/Next.js Best Practices

### 1. Component Structure

**✅ Good:**
```typescript
// Clear prop types
interface TaskListProps {
  tasks: Task[]
  onEdit: (task: Task) => void
}

// Functional component with TypeScript
export default function TaskList({ tasks, onEdit }: TaskListProps) {
  // Hooks at the top
  const [filter, setFilter] = useState('all')
  
  // Early returns for loading/error states
  if (tasks.length === 0) {
    return <EmptyState />
  }
  
  // Main render
  return (
    <div>
      {tasks.map(task => (
        <TaskItem key={task.id} task={task} onEdit={onEdit} />
      ))}
    </div>
  )
}
```

**❌ Bad:**
```typescript
export default function TaskList(props: any) {  // any type!
  // No prop validation
  // Hooks after conditional logic
  if (condition) {
    const [state, setState] = useState()  // ❌ Conditional hook
  }
  
  return (
    <div>
      {props.tasks.map(task => (
        <div onClick={() => {
          // Inline complex logic
          // Multiple lines of code
        }}>
          {task.title}
        </div>
      ))}
    </div>
  )
}
```

### 2. State Management

**✅ Good:**
```typescript
// Zustand store with clear structure
interface TaskState {
  tasks: Task[]
  isLoading: boolean
  error: string | null
  fetchTasks: () => Promise<void>
}

export const useTaskStore = create<TaskState>((set) => ({
  tasks: [],
  isLoading: false,
  error: null,
  
  fetchTasks: async () => {
    set({ isLoading: true, error: null })
    try {
      const tasks = await tasksAPI.list()
      set({ tasks, isLoading: false })
    } catch (error) {
      set({ error: error.message, isLoading: false })
    }
  }
}))
```

**❌ Bad:**
```typescript
// Global variables
let tasks = []

// Mutation without tracking
function addTask(task) {
  tasks.push(task)  // No re-render!
}
```

### 3. API Calls

**✅ Good:**
```typescript
// Centralized API client
export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
})

// Interceptors for auth
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Type-safe API functions
export const tasksAPI = {
  list: async (): Promise<Task[]> => {
    const response = await api.get('/tasks/')
    return response.data
  }
}
```

**❌ Bad:**
```typescript
// Scattered fetch calls
fetch('http://localhost:8000/api/tasks')  // Hardcoded URL!
  .then(res => res.json())
  .then(data => {
    // No error handling
    // No type safety
  })
```

---

## API Design Best Practices

### 1. RESTful Endpoints

**✅ Good:**
```
GET    /api/v1/tasks/           # List tasks
POST   /api/v1/tasks/           # Create task
GET    /api/v1/tasks/{id}/      # Get task
PUT    /api/v1/tasks/{id}/      # Update task (full)
PATCH  /api/v1/tasks/{id}/      # Update task (partial)
DELETE /api/v1/tasks/{id}/      # Delete task

# Custom actions use verbs
POST   /api/v1/tasks/{id}/complete/
GET    /api/v1/tasks/statistics/
```

**❌ Bad:**
```
GET    /api/v1/getTasks          # Not RESTful
POST   /api/v1/createTask        # Not RESTful
GET    /api/v1/task/delete/{id}  # Wrong method
```

### 2. Response Format

**✅ Good:**
```json
{
  "count": 100,
  "next": "http://api.example.com/tasks/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Task",
      "created_at": "2024-01-01T10:00:00Z"
    }
  ]
}
```

**❌ Bad:**
```json
{
  "data": {
    "taskList": [/* tasks */],
    "total": 100,
    "nextPage": 2
  }
}
```

### 3. Error Handling

**✅ Good:**
```json
{
  "error": true,
  "message": "Validation error",
  "status_code": 400,
  "details": {
    "email": ["This field is required."],
    "password": ["Password is too short."]
  }
}
```

**❌ Bad:**
```json
{
  "error": "Something went wrong"
}
```

---

## Database Best Practices

### 1. Indexing

**✅ Good:**
```python
class Task(models.Model):
    # ... fields ...
    
    class Meta:
        indexes = [
            # Index frequently queried fields
            models.Index(fields=['user', 'status']),
            models.Index(fields=['due_date']),
            # Index for sorting
            models.Index(fields=['-created_at']),
        ]
```

### 2. Query Optimization

**✅ Good:**
```python
# Use select_related for foreign keys (JOIN)
tasks = Task.objects.select_related('user', 'category').all()

# Use prefetch_related for reverse relations
users = User.objects.prefetch_related('tasks').all()

# Use only() to fetch specific fields
tasks = Task.objects.only('id', 'title').all()

# Use values() for dictionaries
task_data = Task.objects.values('id', 'title')
```

**❌ Bad:**
```python
# N+1 query problem
tasks = Task.objects.all()
for task in tasks:
    print(task.user.email)  # New query each time!
```

### 3. Migrations

**✅ Good:**
```python
# Always review migrations before applying
python manage.py makemigrations
python manage.py sqlmigrate tasks 0001
python manage.py migrate

# Use data migrations for complex changes
python manage.py makemigrations --empty tasks
```

**❌ Bad:**
```python
# Editing migration files manually
# Deleting migration files
# Not committing migrations to git
```

---

## Security Best Practices

### 1. Authentication

**✅ Good:**
```python
# Use JWT with expiration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
}

# Hash passwords
user.set_password(password)  # Uses PBKDF2

# Validate password strength
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
]
```

### 2. Input Validation

**✅ Good:**
```python
class TaskSerializer(serializers.ModelSerializer):
    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Title too short")
        return value
```

**❌ Bad:**
```python
# Trusting user input
Task.objects.create(
    title=request.POST.get('title'),  # No validation!
)
```

### 3. CORS & CSRF

**✅ Good:**
```python
# Specific origins
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
]

# CSRF protection
MIDDLEWARE = [
    'django.middleware.csrf.CsrfViewMiddleware',
]
```

**❌ Bad:**
```python
CORS_ALLOW_ALL_ORIGINS = True  # Dangerous!
CSRF_COOKIE_SECURE = False  # Not for production
```

---

## Testing Best Practices

### 1. Test Structure

**✅ Good:**
```python
@pytest.mark.django_db
class TestTaskCreation:
    """Group related tests."""
    
    def test_create_task_success(self, authenticated_client):
        """Test successful task creation."""
        # Arrange
        payload = {'title': 'Test', 'priority': 'high'}
        
        # Act
        response = authenticated_client.post('/api/v1/tasks/', payload)
        
        # Assert
        assert response.status_code == 201
        assert response.data['title'] == payload['title']
```

### 2. Use Fixtures

**✅ Good:**
```python
@pytest.fixture
def user(db):
    return User.objects.create_user(
        email='test@example.com',
        password='testpass123'
    )

def test_with_user(user):
    # User is automatically created
    assert user.email == 'test@example.com'
```

### 3. Test Coverage

**✅ Good:**
```bash
# Aim for 80%+ coverage
pytest --cov=apps --cov-report=html

# Test critical paths 100%
pytest --cov=apps.users.views --cov-fail-under=100
```

---

## Performance Best Practices

### 1. Caching

**✅ Good:**
```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # 15 minutes
def task_list(request):
    # Expensive operation
    return JsonResponse(data)

# Redis for sessions
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

### 2. Frontend Optimization

**✅ Good:**
```typescript
// Lazy load components
const TaskModal = dynamic(() => import('@/components/TaskModal'))

// Memoize expensive calculations
const sortedTasks = useMemo(() => {
  return tasks.sort((a, b) => a.priority - b.priority)
}, [tasks])

// Debounce search
const debouncedSearch = useMemo(
  () => debounce((value) => search(value), 300),
  []
)
```

---

## DevOps Best Practices

### 1. Docker

**✅ Good:**
```dockerfile
# Multi-stage build
FROM python:3.11-slim as base
# ... base setup ...

# Production image
FROM base as production
USER appuser  # Non-root user
```

### 2. Environment Variables

**✅ Good:**
```bash
# .env.example (committed)
SECRET_KEY=change-this-in-production
DEBUG=False

# .env (not committed)
SECRET_KEY=actual-secret-key
DEBUG=True
```

### 3. CI/CD

**✅ Good:**
```yaml
# Run tests before deploy
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: pytest
  
  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    steps:
      - run: ./deploy.sh
```

---

## Summary Checklist

### Code Quality
- [ ] Follow SOLID principles
- [ ] Use type hints/TypeScript
- [ ] Write documentation
- [ ] Handle errors properly
- [ ] Validate all inputs

### Performance
- [ ] Optimize database queries
- [ ] Use caching where appropriate
- [ ] Lazy load components
- [ ] Optimize images
- [ ] Use CDN for static files

### Security
- [ ] Validate and sanitize inputs
- [ ] Use HTTPS in production
- [ ] Implement proper authentication
- [ ] Set security headers
- [ ] Keep dependencies updated

### Testing
- [ ] Write unit tests
- [ ] Write integration tests
- [ ] Aim for 80%+ coverage
- [ ] Test edge cases
- [ ] Use CI/CD

### DevOps
- [ ] Use Docker
- [ ] Set up CI/CD
- [ ] Monitor application
- [ ] Set up logging
- [ ] Automate backups

---

Following these best practices will help you build maintainable, scalable, and secure applications!
