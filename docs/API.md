# API Documentation

Complete API reference for the Task Manager application.

## Base URL

```
Development: http://localhost:8000/api/v1
Production: https://your-domain.com/api/v1
```

## Authentication

All API requests (except registration and login) require authentication using JWT tokens.

### Headers

```
Authorization: Bearer <access_token>
Content-Type: application/json
```

---

## Authentication Endpoints

### Register User

Create a new user account.

**Endpoint:** `POST /auth/users/`

**Permission:** Public

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "password_confirm": "securepassword123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response:** `201 Created`
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "full_name": "John Doe",
    "bio": "",
    "avatar": null,
    "is_active": true,
    "created_at": "2024-01-01T10:00:00Z",
    "updated_at": "2024-01-01T10:00:00Z"
  }
}
```

**Errors:**
- `400 Bad Request`: Validation error (email already exists, passwords don't match, etc.)

---

### Login

Obtain JWT access and refresh tokens.

**Endpoint:** `POST /auth/token/`

**Permission:** Public

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response:** `200 OK`
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Errors:**
- `401 Unauthorized`: Invalid credentials

---

### Refresh Token

Get a new access token using refresh token.

**Endpoint:** `POST /auth/token/refresh/`

**Permission:** Public

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response:** `200 OK`
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

### Get User Profile

Get current user's profile.

**Endpoint:** `GET /auth/users/me/`

**Permission:** Authenticated

**Response:** `200 OK`
```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "full_name": "John Doe",
  "bio": "Software developer",
  "avatar": "/media/avatars/user1.jpg",
  "is_active": true,
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T10:00:00Z"
}
```

---

### Update User Profile

Update current user's profile.

**Endpoint:** `PATCH /auth/users/me/`

**Permission:** Authenticated

**Request Body:**
```json
{
  "first_name": "Jane",
  "bio": "Full-stack developer"
}
```

**Response:** `200 OK`
```json
{
  "message": "Profile updated successfully",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "Jane",
    "last_name": "Doe",
    "full_name": "Jane Doe",
    "bio": "Full-stack developer",
    "avatar": null,
    "is_active": true,
    "created_at": "2024-01-01T10:00:00Z",
    "updated_at": "2024-01-01T11:00:00Z"
  }
}
```

---

### Change Password

Change current user's password.

**Endpoint:** `POST /auth/users/change_password/`

**Permission:** Authenticated

**Request Body:**
```json
{
  "old_password": "oldpassword123",
  "new_password": "newpassword123",
  "new_password_confirm": "newpassword123"
}
```

**Response:** `200 OK`
```json
{
  "message": "Password changed successfully"
}
```

**Errors:**
- `400 Bad Request`: Old password incorrect or new passwords don't match

---

## Task Endpoints

### List Tasks

Get all tasks for the current user with optional filtering.

**Endpoint:** `GET /tasks/`

**Permission:** Authenticated

**Query Parameters:**
- `status` (optional): Filter by status (`todo`, `in_progress`, `done`)
- `priority` (optional): Filter by priority (`low`, `medium`, `high`, `urgent`)
- `category` (optional): Filter by category ID
- `overdue` (optional): Filter overdue tasks (`true`)
- `search` (optional): Search in title and description
- `ordering` (optional): Order by field (e.g., `-created_at`, `due_date`)
- `page` (optional): Page number for pagination
- `page_size` (optional): Items per page

**Examples:**
```
GET /tasks/?status=in_progress
GET /tasks/?priority=high&overdue=true
GET /tasks/?search=project&ordering=-created_at
```

**Response:** `200 OK`
```json
{
  "count": 45,
  "next": "http://localhost:8000/api/v1/tasks/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Complete project documentation",
      "status": "in_progress",
      "priority": "high",
      "category_name": "Work",
      "due_date": "2024-12-31T23:59:59Z",
      "is_overdue": false,
      "created_at": "2024-01-01T10:00:00Z",
      "updated_at": "2024-01-01T10:00:00Z"
    }
  ]
}
```

---

### Get Task Detail

Get a specific task by ID.

**Endpoint:** `GET /tasks/{id}/`

**Permission:** Authenticated (own tasks only)

**Response:** `200 OK`
```json
{
  "id": 1,
  "title": "Complete project documentation",
  "description": "Write comprehensive docs for the project",
  "status": "in_progress",
  "priority": "high",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe"
  },
  "category": {
    "id": 1,
    "name": "Work",
    "description": "Work-related tasks",
    "color": "#3B82F6"
  },
  "due_date": "2024-12-31T23:59:59Z",
  "completed_at": null,
  "is_overdue": false,
  "comments": [
    {
      "id": 1,
      "user": {
        "id": 1,
        "email": "user@example.com",
        "full_name": "John Doe"
      },
      "text": "Making good progress!",
      "created_at": "2024-01-02T10:00:00Z",
      "updated_at": "2024-01-02T10:00:00Z"
    }
  ],
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T10:00:00Z"
}
```

**Errors:**
- `404 Not Found`: Task doesn't exist or doesn't belong to user

---

### Create Task

Create a new task.

**Endpoint:** `POST /tasks/`

**Permission:** Authenticated

**Request Body:**
```json
{
  "title": "New task",
  "description": "Task description",
  "status": "todo",
  "priority": "medium",
  "category": 1,
  "due_date": "2024-12-31T23:59:59Z"
}
```

**Response:** `201 Created`
```json
{
  "id": 2,
  "title": "New task",
  "description": "Task description",
  "status": "todo",
  "priority": "medium",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe"
  },
  "category": {
    "id": 1,
    "name": "Work",
    "color": "#3B82F6"
  },
  "due_date": "2024-12-31T23:59:59Z",
  "completed_at": null,
  "is_overdue": false,
  "comments": [],
  "created_at": "2024-01-03T10:00:00Z",
  "updated_at": "2024-01-03T10:00:00Z"
}
```

**Validation:**
- `title`: Required, max 255 characters
- `status`: Must be `todo`, `in_progress`, or `done`
- `priority`: Must be `low`, `medium`, `high`, or `urgent`
- `category`: Must be a valid category ID or null
- `due_date`: Must be ISO 8601 datetime string or null

---

### Update Task

Update an existing task.

**Endpoint:** `PATCH /tasks/{id}/`

**Permission:** Authenticated (own tasks only)

**Request Body:** (all fields optional)
```json
{
  "title": "Updated title",
  "status": "done",
  "priority": "urgent"
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "title": "Updated title",
  "status": "done",
  "priority": "urgent",
  "completed_at": "2024-01-03T10:00:00Z",
  ...
}
```

**Note:** When status changes to `done`, `completed_at` is automatically set.

---

### Delete Task

Delete a task.

**Endpoint:** `DELETE /tasks/{id}/`

**Permission:** Authenticated (own tasks only)

**Response:** `204 No Content`

---

### Get Task Statistics

Get statistics about user's tasks.

**Endpoint:** `GET /tasks/statistics/`

**Permission:** Authenticated

**Response:** `200 OK`
```json
{
  "total": 25,
  "by_status": {
    "todo": 10,
    "in_progress": 8,
    "done": 7
  },
  "by_priority": {
    "low": 5,
    "medium": 12,
    "high": 6,
    "urgent": 2
  },
  "overdue": 3
}
```

---

### Get Overdue Tasks

Get all overdue tasks.

**Endpoint:** `GET /tasks/overdue/`

**Permission:** Authenticated

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "title": "Overdue task",
    "status": "in_progress",
    "priority": "high",
    "due_date": "2023-12-01T23:59:59Z",
    "is_overdue": true,
    ...
  }
]
```

---

### Add Comment to Task

Add a comment to a task.

**Endpoint:** `POST /tasks/{id}/add_comment/`

**Permission:** Authenticated (own tasks only)

**Request Body:**
```json
{
  "text": "This is a comment"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "task": 1,
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe"
  },
  "text": "This is a comment",
  "created_at": "2024-01-03T10:00:00Z",
  "updated_at": "2024-01-03T10:00:00Z"
}
```

---

## Category Endpoints

### List Categories

Get all categories.

**Endpoint:** `GET /tasks/categories/`

**Permission:** Authenticated

**Response:** `200 OK`
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Work",
      "description": "Work-related tasks",
      "color": "#3B82F6",
      "task_count": 15,
      "created_at": "2024-01-01T10:00:00Z",
      "updated_at": "2024-01-01T10:00:00Z"
    }
  ]
}
```

---

### Create Category

Create a new category.

**Endpoint:** `POST /tasks/categories/`

**Permission:** Authenticated

**Request Body:**
```json
{
  "name": "Personal",
  "description": "Personal tasks",
  "color": "#10B981"
}
```

**Response:** `201 Created`
```json
{
  "id": 2,
  "name": "Personal",
  "description": "Personal tasks",
  "color": "#10B981",
  "task_count": 0,
  "created_at": "2024-01-03T10:00:00Z",
  "updated_at": "2024-01-03T10:00:00Z"
}
```

---

## Error Responses

### 400 Bad Request

```json
{
  "error": true,
  "message": "Validation error",
  "status_code": 400,
  "details": {
    "email": ["This field is required."],
    "password": ["This password is too short."]
  }
}
```

### 401 Unauthorized

```json
{
  "error": true,
  "message": "Authentication credentials were not provided.",
  "status_code": 401
}
```

### 403 Forbidden

```json
{
  "error": true,
  "message": "You do not have permission to perform this action.",
  "status_code": 403
}
```

### 404 Not Found

```json
{
  "error": true,
  "message": "Not found.",
  "status_code": 404
}
```

### 500 Internal Server Error

```json
{
  "error": true,
  "message": "An internal server error occurred.",
  "status_code": 500
}
```

---

## Rate Limiting

- **Unauthenticated requests:** 100 requests/hour
- **Authenticated requests:** 1000 requests/hour

Rate limit headers:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

---

## Interactive API Documentation

Visit the following URLs for interactive API documentation:

- **Swagger UI:** http://localhost:8000/api/docs/
- **OpenAPI Schema:** http://localhost:8000/api/schema/

These provide a user-friendly interface to explore and test all API endpoints.
