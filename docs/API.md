# API Documentation

## Base URL
```
http://localhost:5000/api
```

## Authentication

All authenticated endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer <access_token>
```

---

## Authentication Endpoints

### Register User

Create a new user account.

**Endpoint:** `POST /auth/register`

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "SecurePass123",
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
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe",
    "is_active": true,
    "is_admin": false,
    "created_at": "2024-01-01T00:00:00"
  },
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Error Responses:**
- `400 Bad Request` - Invalid input data
- `409 Conflict` - Email or username already exists

---

### Login

Authenticate and receive access tokens.

**Endpoint:** `POST /auth/login`

**Request Body:**
```json
{
  "username": "johndoe",
  "password": "SecurePass123"
}
```

**Response:** `200 OK`
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "user@example.com"
  },
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Error Responses:**
- `400 Bad Request` - Missing credentials
- `401 Unauthorized` - Invalid credentials
- `403 Forbidden` - Account disabled

---

### Refresh Token

Get a new access token using refresh token.

**Endpoint:** `POST /auth/refresh`

**Headers:**
```
Authorization: Bearer <refresh_token>
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

### Logout

Invalidate the current access token.

**Endpoint:** `POST /auth/logout`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
{
  "message": "Logout successful"
}
```

---

### Get Current User

Retrieve the authenticated user's profile.

**Endpoint:** `GET /auth/me`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
{
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "avatar_url": "https://example.com/avatar.jpg",
    "is_active": true,
    "created_at": "2024-01-01T00:00:00",
    "last_login": "2024-01-01T12:00:00"
  }
}
```

---

## User Endpoints

### Get Users

Retrieve a paginated list of users.

**Endpoint:** `GET /users`

**Query Parameters:**
- `page` (integer, default: 1) - Page number
- `per_page` (integer, default: 20) - Items per page
- `search` (string, optional) - Search by username or email

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
{
  "users": [
    {
      "id": 1,
      "username": "johndoe",
      "first_name": "John",
      "last_name": "Doe",
      "avatar_url": "https://example.com/avatar.jpg",
      "is_active": true,
      "created_at": "2024-01-01T00:00:00"
    }
  ],
  "total": 50,
  "pages": 3,
  "current_page": 1
}
```

---

### Get User by ID

Retrieve a specific user's profile.

**Endpoint:** `GET /users/{user_id}`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
{
  "user": {
    "id": 1,
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe",
    "avatar_url": "https://example.com/avatar.jpg",
    "is_active": true,
    "created_at": "2024-01-01T00:00:00"
  }
}
```

**Error Responses:**
- `404 Not Found` - User not found

---

### Update Profile

Update the authenticated user's profile.

**Endpoint:** `PUT /users/profile`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "avatar_url": "https://example.com/new-avatar.jpg"
}
```

**Response:** `200 OK`
```json
{
  "message": "Profile updated successfully",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "avatar_url": "https://example.com/new-avatar.jpg"
  }
}
```

---

## Task Endpoints

### Get Tasks

Retrieve a filtered and paginated list of tasks for the authenticated user.

**Endpoint:** `GET /tasks`

**Query Parameters:**
- `page` (integer, default: 1) - Page number
- `per_page` (integer, default: 20) - Items per page
- `status` (string, optional) - Filter by status: `pending`, `in_progress`, `completed`, `cancelled`
- `priority` (string, optional) - Filter by priority: `low`, `medium`, `high`, `urgent`
- `search` (string, optional) - Search in task titles

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Complete project",
      "description": "Finish the full stack application",
      "status": "in_progress",
      "priority": "high",
      "due_date": "2024-12-31T23:59:59",
      "completed_at": null,
      "user_id": 1,
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-02T00:00:00",
      "tags": ["work", "important"]
    }
  ],
  "total": 25,
  "pages": 2,
  "current_page": 1
}
```

---

### Get Task by ID

Retrieve a specific task.

**Endpoint:** `GET /tasks/{task_id}`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
{
  "task": {
    "id": 1,
    "title": "Complete project",
    "description": "Finish the full stack application",
    "status": "in_progress",
    "priority": "high",
    "due_date": "2024-12-31T23:59:59",
    "completed_at": null,
    "user_id": 1,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-02T00:00:00",
    "tags": ["work", "important"]
  }
}
```

**Error Responses:**
- `404 Not Found` - Task not found

---

### Create Task

Create a new task.

**Endpoint:** `POST /tasks`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "title": "Complete project",
  "description": "Finish the full stack application",
  "status": "in_progress",
  "priority": "high",
  "due_date": "2024-12-31T23:59:59Z",
  "tags": ["work", "important"]
}
```

**Response:** `201 Created`
```json
{
  "message": "Task created successfully",
  "task": {
    "id": 1,
    "title": "Complete project",
    "description": "Finish the full stack application",
    "status": "in_progress",
    "priority": "high",
    "due_date": "2024-12-31T23:59:59",
    "tags": ["work", "important"]
  }
}
```

**Error Responses:**
- `400 Bad Request` - Missing or invalid data

---

### Update Task

Update an existing task.

**Endpoint:** `PUT /tasks/{task_id}`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "title": "Updated task title",
  "status": "completed",
  "priority": "medium"
}
```

**Response:** `200 OK`
```json
{
  "message": "Task updated successfully",
  "task": {
    "id": 1,
    "title": "Updated task title",
    "status": "completed",
    "priority": "medium",
    "completed_at": "2024-01-03T10:00:00"
  }
}
```

**Error Responses:**
- `404 Not Found` - Task not found
- `400 Bad Request` - Invalid data

---

### Delete Task

Delete a task.

**Endpoint:** `DELETE /tasks/{task_id}`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
{
  "message": "Task deleted successfully"
}
```

**Error Responses:**
- `404 Not Found` - Task not found

---

### Get Tags

Retrieve all available tags.

**Endpoint:** `GET /tasks/tags`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
{
  "tags": [
    {
      "id": 1,
      "name": "work",
      "color": "#3B82F6",
      "created_at": "2024-01-01T00:00:00"
    },
    {
      "id": 2,
      "name": "important",
      "color": "#EF4444",
      "created_at": "2024-01-01T00:00:00"
    }
  ]
}
```

---

## Analytics Endpoints

### Dashboard Statistics

Get dashboard statistics for the authenticated user.

**Endpoint:** `GET /analytics/dashboard`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
{
  "total_tasks": 25,
  "completed_this_week": 5,
  "overdue_tasks": 2,
  "status_distribution": {
    "pending": 10,
    "in_progress": 8,
    "completed": 6,
    "cancelled": 1
  },
  "priority_distribution": {
    "low": 5,
    "medium": 12,
    "high": 6,
    "urgent": 2
  }
}
```

---

### Productivity Metrics

Get productivity statistics over time.

**Endpoint:** `GET /analytics/productivity`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
{
  "daily_completed": [
    {
      "date": "2024-01-01",
      "count": 3
    },
    {
      "date": "2024-01-02",
      "count": 5
    }
  ]
}
```

---

## WebSocket Events

Connect to WebSocket for real-time updates:

```javascript
const socket = io('http://localhost:5000', {
  auth: {
    token: 'your-access-token'
  }
})
```

### Events

**task_created**
Emitted when a new task is created.

**task_updated**
Emitted when a task is updated.

**task_deleted**
Emitted when a task is deleted.

---

## Error Responses

All endpoints may return the following error responses:

**400 Bad Request**
```json
{
  "error": "Bad request",
  "message": "Detailed error message"
}
```

**401 Unauthorized**
```json
{
  "error": "Unauthorized",
  "message": "Invalid or missing token"
}
```

**403 Forbidden**
```json
{
  "error": "Forbidden",
  "message": "Insufficient permissions"
}
```

**404 Not Found**
```json
{
  "error": "Not found",
  "message": "Resource not found"
}
```

**500 Internal Server Error**
```json
{
  "error": "Internal server error",
  "message": "An unexpected error occurred"
}
```
