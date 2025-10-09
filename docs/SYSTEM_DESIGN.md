# System Design & Architecture

This document explains the system design concepts and architectural decisions in this application.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Database Design](#database-design)
3. [API Design](#api-design)
4. [Authentication & Authorization](#authentication--authorization)
5. [Scalability Considerations](#scalability-considerations)
6. [Performance Optimization](#performance-optimization)
7. [Security Design](#security-design)

---

## Architecture Overview

### High-Level Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                        Client Layer                          │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │  Browser   │  │   Mobile   │  │   Desktop  │            │
│  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘            │
│        │                │                │                    │
└────────┼────────────────┼────────────────┼────────────────────┘
         │                │                │
         └────────────────┴────────────────┘
                         │
                    HTTP/HTTPS
                         │
         ┌───────────────▼────────────────┐
         │      Load Balancer (Nginx)     │
         └───────────────┬────────────────┘
                         │
         ┌───────────────▼────────────────┐
         │    Application Layer           │
         │  ┌──────────┐  ┌──────────┐   │
         │  │ Next.js  │  │  Django  │   │
         │  │ Frontend │  │  Backend │   │
         │  └──────────┘  └─────┬────┘   │
         └──────────────────────┼─────────┘
                                │
         ┌──────────────────────▼─────────┐
         │      Data Layer                │
         │  ┌──────────┐  ┌──────────┐   │
         │  │PostgreSQL│  │  Redis   │   │
         │  │ Database │  │  Cache   │   │
         │  └──────────┘  └──────────┘   │
         └────────────────────────────────┘
```

### Technology Stack Rationale

#### Backend: Django + Django REST Framework

**Why Django?**
- **Batteries included:** Admin panel, ORM, authentication out of the box
- **Security:** Built-in protection against SQL injection, XSS, CSRF
- **Scalability:** Used by Instagram, Pinterest, Mozilla
- **ORM:** Powerful database abstraction
- **Community:** Large ecosystem and third-party packages

**Why Django REST Framework?**
- **Serialization:** Easy data transformation
- **ViewSets:** Automatic CRUD endpoints
- **Authentication:** Multiple auth backends
- **Documentation:** Auto-generated API docs
- **Browsable API:** Built-in API explorer

#### Frontend: Next.js + TypeScript

**Why Next.js?**
- **Performance:** Server-side rendering (SSR) and static site generation (SSG)
- **SEO:** Better search engine optimization
- **File-based routing:** Intuitive page structure
- **API Routes:** Backend functionality in Next.js
- **Image optimization:** Automatic image optimization
- **Developer experience:** Hot reloading, error handling

**Why TypeScript?**
- **Type safety:** Catch errors at compile time
- **IntelliSense:** Better IDE support
- **Refactoring:** Safer code changes
- **Documentation:** Types serve as documentation
- **Scalability:** Better for large codebases

#### Database: PostgreSQL

**Why PostgreSQL?**
- **ACID compliance:** Data integrity
- **Advanced features:** JSON support, full-text search, arrays
- **Performance:** Excellent query optimization
- **Reliability:** Battle-tested in production
- **Open source:** No licensing costs

---

## Database Design

### Entity Relationship Diagram (ERD)

```
┌─────────────────┐
│      User       │
├─────────────────┤
│ id (PK)         │
│ email (unique)  │
│ first_name      │
│ last_name       │
│ password_hash   │
│ bio             │
│ avatar          │
│ created_at      │
│ updated_at      │
└────────┬────────┘
         │
         │ 1:N
         │
┌────────▼────────┐      N:1      ┌─────────────────┐
│      Task       │◄───────────────│    Category     │
├─────────────────┤                ├─────────────────┤
│ id (PK)         │                │ id (PK)         │
│ title           │                │ name            │
│ description     │                │ description     │
│ status          │                │ color           │
│ priority        │                │ created_at      │
│ user_id (FK)    │                │ updated_at      │
│ category_id(FK) │                └─────────────────┘
│ due_date        │
│ completed_at    │
│ created_at      │
│ updated_at      │
└────────┬────────┘
         │
         │ 1:N
         │
┌────────▼────────┐
│    Comment      │
├─────────────────┤
│ id (PK)         │
│ task_id (FK)    │
│ user_id (FK)    │
│ text            │
│ created_at      │
│ updated_at      │
└─────────────────┘
```

### Database Normalization

Our database follows **Third Normal Form (3NF)**:

1. **First Normal Form (1NF):**
   - All columns contain atomic values
   - Each column has a unique name
   - Order doesn't matter

2. **Second Normal Form (2NF):**
   - Meets 1NF
   - No partial dependencies (all non-key attributes depend on the entire primary key)

3. **Third Normal Form (3NF):**
   - Meets 2NF
   - No transitive dependencies (non-key attributes don't depend on other non-key attributes)

**Example:**
```python
# Good - 3NF compliant
class Task(models.Model):
    user = models.ForeignKey(User)  # Reference, not duplicate data
    category = models.ForeignKey(Category)  # Reference, not duplicate data

# Bad - Not normalized
class Task(models.Model):
    user_email = models.EmailField()  # Duplicate from User table
    category_name = models.CharField()  # Duplicate from Category table
```

### Indexing Strategy

```python
class Task(models.Model):
    # ... fields ...
    
    class Meta:
        indexes = [
            # Composite index for common queries
            models.Index(fields=['user', 'status']),
            
            # Index for date-based queries
            models.Index(fields=['due_date']),
            
            # Index for sorting
            models.Index(fields=['-created_at']),
        ]
```

**Why indexing matters:**
- **Query Performance:** 10-100x faster queries
- **Common Query Patterns:** Index fields used in WHERE, JOIN, ORDER BY
- **Trade-offs:** Slower writes, more storage (acceptable for read-heavy apps)

---

## API Design

### RESTful API Principles

Our API follows REST (Representational State Transfer) principles:

1. **Resource-Based URLs**
```
✅ Good: GET /api/v1/tasks/123
❌ Bad:  GET /api/v1/getTasks?id=123

✅ Good: POST /api/v1/tasks/
❌ Bad:  POST /api/v1/createTask
```

2. **HTTP Methods**
- `GET`: Retrieve resources
- `POST`: Create resources
- `PUT/PATCH`: Update resources
- `DELETE`: Delete resources

3. **Status Codes**
```python
200 OK              # Successful GET, PUT, PATCH
201 Created         # Successful POST
204 No Content      # Successful DELETE
400 Bad Request     # Invalid input
401 Unauthorized    # Authentication required
403 Forbidden       # Permission denied
404 Not Found       # Resource doesn't exist
500 Server Error    # Server-side error
```

### API Versioning

```python
# URL-based versioning (our approach)
/api/v1/tasks/
/api/v2/tasks/  # Future version

# Why versioning?
# - Backward compatibility
# - Gradual migration
# - Multiple client versions
```

### Request/Response Format

**Request:**
```json
POST /api/v1/tasks/
Content-Type: application/json
Authorization: Bearer <token>

{
  "title": "Complete project",
  "description": "Finish the task manager",
  "priority": "high",
  "due_date": "2024-12-31T23:59:59Z"
}
```

**Response:**
```json
HTTP/1.1 201 Created
Content-Type: application/json

{
  "id": 1,
  "title": "Complete project",
  "description": "Finish the task manager",
  "status": "todo",
  "priority": "high",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe"
  },
  "category": null,
  "due_date": "2024-12-31T23:59:59Z",
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T10:00:00Z"
}
```

### Pagination

```python
# Django REST Framework pagination
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# Response format
{
  "count": 100,
  "next": "http://api.example.com/tasks/?page=2",
  "previous": null,
  "results": [
    { /* task 1 */ },
    { /* task 2 */ },
    // ... 20 items
  ]
}
```

### Filtering & Searching

```python
# URL parameters for filtering
GET /api/v1/tasks/?status=in_progress
GET /api/v1/tasks/?priority=high
GET /api/v1/tasks/?search=project
GET /api/v1/tasks/?ordering=-created_at

# Implementation
class TaskViewSet(viewsets.ModelViewSet):
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'due_date', 'priority']
```

---

## Authentication & Authorization

### JWT Authentication Flow

```
┌─────────┐                                      ┌─────────┐
│ Client  │                                      │ Server  │
└────┬────┘                                      └────┬────┘
     │                                                 │
     │  POST /api/v1/auth/token/                      │
     │  { email, password }                           │
     ├────────────────────────────────────────────────►
     │                                                 │
     │         Validate credentials                    │
     │         Generate JWT tokens                     │
     │                                                 │
     │  { access: "...", refresh: "..." }             │
     ◄────────────────────────────────────────────────┤
     │                                                 │
     │  Store tokens in localStorage                   │
     │                                                 │
     │  GET /api/v1/tasks/                            │
     │  Authorization: Bearer <access_token>          │
     ├────────────────────────────────────────────────►
     │                                                 │
     │         Verify JWT signature                    │
     │         Extract user from token                 │
     │                                                 │
     │  { tasks: [...] }                              │
     ◄────────────────────────────────────────────────┤
     │                                                 │
     │  (Access token expires)                         │
     │                                                 │
     │  POST /api/v1/auth/token/refresh/              │
     │  { refresh: "..." }                            │
     ├────────────────────────────────────────────────►
     │                                                 │
     │         Verify refresh token                    │
     │         Generate new access token               │
     │                                                 │
     │  { access: "..." }                             │
     ◄────────────────────────────────────────────────┤
```

### JWT Token Structure

```
Header.Payload.Signature

# Header
{
  "alg": "HS256",
  "typ": "JWT"
}

# Payload
{
  "user_id": 1,
  "email": "user@example.com",
  "exp": 1640995200,  # Expiration timestamp
  "iat": 1640991600   # Issued at timestamp
}

# Signature
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  secret_key
)
```

### Authorization Levels

```python
# 1. Public endpoints (no authentication)
permission_classes = [AllowAny]

# 2. Authenticated users only
permission_classes = [IsAuthenticated]

# 3. Object-level permissions
class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions for any request
        if request.method in SAFE_METHODS:
            return True
        
        # Write permissions only for owner
        return obj.user == request.user
```

---

## Scalability Considerations

### Horizontal vs Vertical Scaling

**Vertical Scaling (Scale Up):**
```
┌──────────┐        ┌──────────┐
│  4GB RAM │   →    │ 16GB RAM │
│  2 Cores │        │  8 Cores │
└──────────┘        └──────────┘
```
- Pros: Simple, no code changes
- Cons: Hardware limits, single point of failure

**Horizontal Scaling (Scale Out):**
```
┌──────────┐        ┌──────────┐  ┌──────────┐  ┌──────────┐
│ Server 1 │   →    │ Server 1 │  │ Server 2 │  │ Server 3 │
└──────────┘        └──────────┘  └──────────┘  └──────────┘
```
- Pros: No limits, redundancy, better availability
- Cons: Complexity, session management

### Load Balancing

```
                    ┌─────────────┐
                    │Load Balancer│
                    └──────┬──────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
    ┌────▼────┐       ┌────▼────┐       ┌───▼─────┐
    │Server 1 │       │Server 2 │       │Server 3 │
    └────┬────┘       └────┬────┘       └────┬────┘
         │                 │                 │
         └─────────────────┼─────────────────┘
                           │
                    ┌──────▼──────┐
                    │  Database   │
                    └─────────────┘
```

**Strategies:**
- Round Robin: Distribute evenly
- Least Connections: Route to server with fewest connections
- IP Hash: Same client → same server (session persistence)

### Caching Strategy

```python
# 1. Database query caching
from django.core.cache import cache

def get_user_tasks(user_id):
    cache_key = f'user_tasks_{user_id}'
    tasks = cache.get(cache_key)
    
    if tasks is None:
        tasks = Task.objects.filter(user_id=user_id)
        cache.set(cache_key, tasks, timeout=300)  # 5 minutes
    
    return tasks

# 2. Redis for session storage
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

### Database Optimization

**1. Query Optimization:**
```python
# Bad: N+1 queries
tasks = Task.objects.all()
for task in tasks:
    print(task.user.email)  # Query for each task!

# Good: Use select_related (JOIN)
tasks = Task.objects.select_related('user', 'category')
for task in tasks:
    print(task.user.email)  # No extra queries

# Good: Use prefetch_related (separate queries)
tasks = Task.objects.prefetch_related('comments')
```

**2. Database Connection Pooling:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'CONN_MAX_AGE': 600,  # Reuse connections for 10 minutes
    }
}
```

---

## Performance Optimization

### Frontend Optimization

**1. Code Splitting:**
```typescript
// Lazy load components
const TaskModal = dynamic(() => import('@/components/TaskModal'))

// Only load when needed
{showModal && <TaskModal />}
```

**2. Image Optimization:**
```typescript
import Image from 'next/image'

// Next.js automatically optimizes images
<Image 
  src="/avatar.jpg" 
  width={200} 
  height={200}
  alt="User avatar"
/>
```

**3. Memoization:**
```typescript
// Prevent unnecessary re-renders
const ExpensiveComponent = memo(({ data }) => {
  // ... expensive rendering
})

// Memoize calculations
const sortedTasks = useMemo(() => {
  return tasks.sort((a, b) => a.priority - b.priority)
}, [tasks])
```

### Backend Optimization

**1. Database Indexing:**
```python
class Meta:
    indexes = [
        models.Index(fields=['user', 'status']),
    ]
```

**2. Async Views (Django 4.1+):**
```python
async def get_tasks(request):
    tasks = await Task.objects.filter(user=request.user).aall()
    return JsonResponse({'tasks': tasks})
```

**3. Pagination:**
```python
# Don't load all data at once
GET /api/v1/tasks/?page=1&page_size=20
```

---

## Security Design

### OWASP Top 10 Mitigations

**1. Injection (SQL, XSS):**
```python
# Django ORM prevents SQL injection
Task.objects.filter(title=user_input)  # Safe

# Template auto-escaping prevents XSS
{{ user_input }}  # Automatically escaped
```

**2. Broken Authentication:**
```python
# Strong password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
]

# JWT with expiration
'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
```

**3. Sensitive Data Exposure:**
```python
# Password hashing
user.set_password(password)  # Uses PBKDF2

# HTTPS in production
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
```

**4. CSRF Protection:**
```python
# Django CSRF middleware
MIDDLEWARE = [
    'django.middleware.csrf.CsrfViewMiddleware',
]
```

**5. Security Headers:**
```python
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000
```

---

## Monitoring & Logging

### Application Monitoring

```python
# Django logging configuration
LOGGING = {
    'version': 1,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/error.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
        },
    },
}
```

### Metrics to Track

1. **Application Metrics:**
   - Request rate
   - Response time
   - Error rate
   - Database query time

2. **Business Metrics:**
   - User registrations
   - Tasks created
   - Active users

3. **Infrastructure Metrics:**
   - CPU usage
   - Memory usage
   - Disk I/O
   - Network traffic

---

This system design provides a solid foundation that can scale from a few users to millions while maintaining performance, security, and maintainability.
