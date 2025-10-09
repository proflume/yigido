"""
Pytest configuration and fixtures.

This demonstrates testing best practices:
- Reusable fixtures
- Factory pattern for test data
- API client setup
"""

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.tasks.models import Category, Task

User = get_user_model()


@pytest.fixture
def api_client():
    """Return an API client for testing."""
    return APIClient()


@pytest.fixture
def user(db):
    """Create a test user."""
    return User.objects.create_user(
        email='test@example.com',
        password='testpass123',
        first_name='Test',
        last_name='User'
    )


@pytest.fixture
def authenticated_client(api_client, user):
    """Return an authenticated API client."""
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def category(db):
    """Create a test category."""
    return Category.objects.create(
        name='Work',
        description='Work-related tasks',
        color='#3B82F6'
    )


@pytest.fixture
def task(db, user, category):
    """Create a test task."""
    return Task.objects.create(
        title='Test Task',
        description='Test task description',
        user=user,
        category=category,
        status=Task.Status.TODO,
        priority=Task.Priority.MEDIUM
    )
