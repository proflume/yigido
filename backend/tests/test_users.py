"""
User API Tests

This demonstrates API testing best practices:
- Testing authentication flows
- Testing CRUD operations
- Testing validation
- Using fixtures for setup
"""

import pytest
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()


@pytest.mark.django_db
class TestUserRegistration:
    """Test user registration endpoint."""
    
    def test_register_user_success(self, api_client):
        """Test successful user registration."""
        payload = {
            'email': 'newuser@example.com',
            'password': 'strongpass123',
            'password_confirm': 'strongpass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        
        response = api_client.post('/api/v1/auth/users/', payload)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert 'user' in response.data
        assert response.data['user']['email'] == payload['email']
        
        # Verify user was created
        user = User.objects.get(email=payload['email'])
        assert user.first_name == payload['first_name']
        assert user.check_password(payload['password'])
    
    def test_register_user_password_mismatch(self, api_client):
        """Test registration fails with password mismatch."""
        payload = {
            'email': 'newuser@example.com',
            'password': 'strongpass123',
            'password_confirm': 'different123',
            'first_name': 'New',
            'last_name': 'User'
        }
        
        response = api_client.post('/api/v1/auth/users/', payload)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_register_user_duplicate_email(self, api_client, user):
        """Test registration fails with duplicate email."""
        payload = {
            'email': user.email,
            'password': 'strongpass123',
            'password_confirm': 'strongpass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        
        response = api_client.post('/api/v1/auth/users/', payload)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUserProfile:
    """Test user profile endpoints."""
    
    def test_get_profile(self, authenticated_client, user):
        """Test getting user profile."""
        response = authenticated_client.get('/api/v1/auth/users/me/')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == user.email
        assert response.data['first_name'] == user.first_name
    
    def test_update_profile(self, authenticated_client, user):
        """Test updating user profile."""
        payload = {
            'first_name': 'Updated',
            'bio': 'New bio'
        }
        
        response = authenticated_client.patch('/api/v1/auth/users/me/', payload)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['user']['first_name'] == payload['first_name']
        
        # Verify database update
        user.refresh_from_db()
        assert user.first_name == payload['first_name']
        assert user.bio == payload['bio']
    
    def test_profile_requires_authentication(self, api_client):
        """Test that profile endpoint requires authentication."""
        response = api_client.get('/api/v1/auth/users/me/')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestPasswordChange:
    """Test password change endpoint."""
    
    def test_change_password_success(self, authenticated_client, user):
        """Test successful password change."""
        payload = {
            'old_password': 'testpass123',
            'new_password': 'newstrongpass123',
            'new_password_confirm': 'newstrongpass123'
        }
        
        response = authenticated_client.post('/api/v1/auth/users/change_password/', payload)
        
        assert response.status_code == status.HTTP_200_OK
        
        # Verify password was changed
        user.refresh_from_db()
        assert user.check_password(payload['new_password'])
    
    def test_change_password_wrong_old_password(self, authenticated_client):
        """Test password change fails with wrong old password."""
        payload = {
            'old_password': 'wrongpassword',
            'new_password': 'newstrongpass123',
            'new_password_confirm': 'newstrongpass123'
        }
        
        response = authenticated_client.post('/api/v1/auth/users/change_password/', payload)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
