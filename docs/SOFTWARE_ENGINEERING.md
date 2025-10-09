# Software Engineering Concepts

This document explains the software engineering principles and best practices implemented in this project.

## Table of Contents

1. [SOLID Principles](#solid-principles)
2. [Design Patterns](#design-patterns)
3. [Clean Architecture](#clean-architecture)
4. [Code Quality](#code-quality)
5. [Testing Strategies](#testing-strategies)

---

## SOLID Principles

SOLID is an acronym for five design principles that make software designs more understandable, flexible, and maintainable.

### 1. Single Responsibility Principle (SRP)

**Definition:** A class should have only one reason to change.

**Example in our project:**

```python
# backend/apps/users/models.py
class User(AbstractUser):
    """
    User model - ONLY handles user data and authentication
    Does NOT handle email sending, logging, etc.
    """
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=500, blank=True)
    # ... user-specific fields only

# backend/apps/users/serializers.py
class UserSerializer(serializers.ModelSerializer):
    """
    UserSerializer - ONLY handles serialization/deserialization
    Does NOT handle business logic or database operations
    """
    # ... serialization logic only
```

**Why it matters:** When each class has a single responsibility, changes to one part of the system don't cascade to other parts, reducing bugs and making maintenance easier.

### 2. Open/Closed Principle (OCP)

**Definition:** Software entities should be open for extension but closed for modification.

**Example in our project:**

```python
# backend/apps/core/exceptions.py
def custom_exception_handler(exc, context):
    """
    Base exception handler - can be extended without modification
    """
    response = exception_handler(exc, context)
    
    if response is not None:
        custom_response_data = {
            'error': True,
            'message': str(exc),
            'status_code': response.status_code
        }
        response.data = custom_response_data
    
    return response

# You can extend this by adding new exception types without modifying the base handler
```

### 3. Liskov Substitution Principle (LSP)

**Definition:** Objects of a superclass should be replaceable with objects of a subclass without breaking the application.

**Example:**

```python
# Different serializers can be used interchangeably
class TaskListSerializer(serializers.ModelSerializer):
    """Lightweight serializer"""
    pass

class TaskDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer"""
    pass

# In the view, we can substitute serializers
def get_serializer_class(self):
    if self.action == 'list':
        return TaskListSerializer
    return TaskDetailSerializer
```

### 4. Interface Segregation Principle (ISP)

**Definition:** Clients should not be forced to depend on interfaces they don't use.

**Example in our project:**

```typescript
// frontend/src/lib/types.ts
// Instead of one large interface, we have specific interfaces

interface User {
  id: number
  email: string
  // ... user-specific fields only
}

interface Task {
  id: number
  title: string
  // ... task-specific fields only
}

// Components only import what they need
```

### 5. Dependency Inversion Principle (DIP)

**Definition:** High-level modules should not depend on low-level modules. Both should depend on abstractions.

**Example:**

```python
# backend/apps/tasks/views.py
class TaskViewSet(viewsets.ModelViewSet):
    """
    Depends on abstract serializer_class, not concrete implementation
    """
    def get_serializer_class(self):
        # Returns different serializers based on action
        # The view doesn't care about the concrete implementation
        pass
```

---

## Design Patterns

Design patterns are reusable solutions to common software design problems.

### 1. Repository Pattern

**Purpose:** Abstracts data access logic.

**Implementation:**

```python
# Django's ORM acts as a repository pattern
# backend/apps/tasks/models.py

class TaskManager(models.Manager):
    """Custom manager acts as a repository"""
    
    def get_user_tasks(self, user):
        return self.filter(user=user)
    
    def get_overdue_tasks(self):
        from django.utils import timezone
        return self.filter(
            due_date__lt=timezone.now(),
            status__in=['todo', 'in_progress']
        )

class Task(models.Model):
    objects = TaskManager()
```

### 2. Factory Pattern

**Purpose:** Create objects without specifying the exact class.

**Implementation:**

```python
# backend/apps/users/models.py
class UserManager(BaseUserManager):
    """Factory for creating users"""
    
    def create_user(self, email, password=None, **extra_fields):
        # Factory method creates different types of users
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        # Different factory method for superusers
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
```

### 3. Observer Pattern

**Purpose:** Define a one-to-many dependency between objects.

**Implementation:**

```typescript
// frontend/src/store/taskStore.ts
// Zustand implements observer pattern

export const useTaskStore = create<TaskState>((set, get) => ({
  tasks: [],
  
  // When state changes, all observers (components) are notified
  fetchTasks: async () => {
    const response = await tasksAPI.list()
    set({ tasks: response.results }) // Notifies all observers
  }
}))

// Components observe the store
function TaskList() {
  const tasks = useTaskStore(state => state.tasks) // Observer
  // Component re-renders when tasks change
}
```

### 4. Strategy Pattern

**Purpose:** Define a family of algorithms and make them interchangeable.

**Implementation:**

```python
# backend/apps/tasks/views.py
class TaskViewSet(viewsets.ModelViewSet):
    """Different strategies for different actions"""
    
    def get_serializer_class(self):
        # Strategy pattern - choose serializer based on action
        if self.action == 'list':
            return TaskListSerializer
        elif self.action == 'create':
            return TaskCreateSerializer
        return TaskDetailSerializer
```

### 5. Decorator Pattern

**Purpose:** Add new functionality to objects dynamically.

**Implementation:**

```python
# Django's @action decorator
from rest_framework.decorators import action

class TaskViewSet(viewsets.ModelViewSet):
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        # Decorator adds custom action to ViewSet
        pass
```

---

## Clean Architecture

Clean Architecture separates concerns into layers, making the system maintainable and testable.

### Layer Structure

```
┌─────────────────────────────────────┐
│         Presentation Layer          │ ← Views, Serializers, Components
├─────────────────────────────────────┤
│         Application Layer           │ ← ViewSets, Business Logic
├─────────────────────────────────────┤
│          Domain Layer               │ ← Models, Core Logic
├─────────────────────────────────────┤
│       Infrastructure Layer          │ ← Database, External APIs
└─────────────────────────────────────┘
```

### Implementation in Our Project

**Domain Layer (Core Business Logic):**
```python
# backend/apps/tasks/models.py
class Task(models.Model):
    """Pure domain model"""
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=Status.choices)
    
    @property
    def is_overdue(self):
        """Business logic stays in the model"""
        if self.due_date and self.status != self.Status.DONE:
            from django.utils import timezone
            return timezone.now() > self.due_date
        return False
```

**Application Layer (Use Cases):**
```python
# backend/apps/tasks/views.py
class TaskViewSet(viewsets.ModelViewSet):
    """Application logic - orchestrates the domain"""
    
    def perform_create(self, serializer):
        # Application logic: set user when creating
        serializer.save(user=self.request.user)
```

**Presentation Layer (Interface):**
```python
# backend/apps/tasks/serializers.py
class TaskSerializer(serializers.ModelSerializer):
    """Presentation logic - how data is presented"""
    
    class Meta:
        model = Task
        fields = '__all__'
```

---

## Code Quality

### 1. DRY (Don't Repeat Yourself)

**Bad:**
```python
# Repeated logic
def view1(request):
    user = request.user
    if not user.is_authenticated:
        return Response(status=401)
    # ...

def view2(request):
    user = request.user
    if not user.is_authenticated:
        return Response(status=401)
    # ...
```

**Good:**
```python
# Reusable permission class
class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]  # Reuse everywhere
```

### 2. KISS (Keep It Simple, Stupid)

**Bad:**
```python
def complex_task_filter(tasks, status, priority, category, user, date_from, date_to):
    # 50 lines of complex filtering logic
    pass
```

**Good:**
```python
# Use Django's built-in queryset methods
def get_queryset(self):
    queryset = Task.objects.filter(user=self.request.user)
    
    status = self.request.query_params.get('status')
    if status:
        queryset = queryset.filter(status=status)
    
    return queryset
```

### 3. YAGNI (You Aren't Gonna Need It)

Don't add functionality until it's necessary. Our project only includes features that are actually used.

### 4. Code Organization

**File Structure:**
- One class per file (when it makes sense)
- Group related functionality
- Clear naming conventions

**Example:**
```
backend/apps/tasks/
├── models.py         # Data models
├── serializers.py    # Data transformation
├── views.py          # Request handling
├── urls.py           # URL routing
└── admin.py          # Admin configuration
```

---

## Testing Strategies

### 1. Test Pyramid

```
        ┌────────┐
        │   E2E  │  ← Few, slow, expensive
        ├────────┤
        │ Integration │  ← Some, medium speed
        ├────────────┤
        │    Unit     │  ← Many, fast, cheap
        └────────────┘
```

### 2. Unit Testing

**Purpose:** Test individual components in isolation.

**Example:**
```python
# backend/tests/test_users.py
@pytest.mark.django_db
class TestUserRegistration:
    def test_register_user_success(self, api_client):
        """Test one specific thing: successful registration"""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            # ...
        }
        
        response = api_client.post('/api/v1/auth/users/', payload)
        
        assert response.status_code == 201
        assert User.objects.filter(email='test@example.com').exists()
```

### 3. Integration Testing

**Purpose:** Test how components work together.

**Example:**
```python
@pytest.mark.django_db
def test_create_task_with_category(authenticated_client, category):
    """Test task creation with category relationship"""
    payload = {
        'title': 'Test Task',
        'category': category.id
    }
    
    response = authenticated_client.post('/api/v1/tasks/', payload)
    
    assert response.status_code == 201
    task = Task.objects.get(id=response.data['id'])
    assert task.category == category
```

### 4. Test Coverage

Aim for:
- 80%+ code coverage
- 100% coverage of critical paths
- All edge cases covered

```bash
# Run with coverage
pytest --cov=apps --cov-report=html
```

### 5. Test Best Practices

1. **AAA Pattern:** Arrange, Act, Assert
```python
def test_example():
    # Arrange - set up test data
    user = create_user()
    
    # Act - perform the action
    result = user.get_full_name()
    
    # Assert - verify the result
    assert result == "John Doe"
```

2. **Use Fixtures:** Reuse test setup
```python
@pytest.fixture
def user(db):
    return User.objects.create_user(email='test@example.com')

def test_with_user(user):
    # user fixture is automatically provided
    assert user.email == 'test@example.com'
```

3. **Test Isolation:** Each test should be independent
```python
@pytest.mark.django_db
def test_1():
    User.objects.create(email='test@example.com')
    # Test logic

@pytest.mark.django_db
def test_2():
    # Starts with clean database
    assert User.objects.count() == 0
```

---

## Conclusion

These software engineering principles and patterns are not just theoretical concepts—they're practical tools that make your code:

- **More maintainable:** Easy to update and fix
- **More testable:** Easy to verify correctness
- **More scalable:** Easy to extend with new features
- **More readable:** Easy for others (and future you) to understand

Study the codebase to see these principles in action!
