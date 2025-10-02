"""
Authentication tests
"""
import pytest
from app import create_app, db
from app.models import User


@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


def test_register_success(client):
    """Test successful user registration"""
    response = client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'username': 'testuser',
        'password': 'Test1234',
        'first_name': 'Test',
        'last_name': 'User'
    })
    
    assert response.status_code == 201
    data = response.get_json()
    assert 'access_token' in data
    assert 'refresh_token' in data
    assert data['user']['username'] == 'testuser'


def test_register_duplicate_email(client):
    """Test registration with duplicate email"""
    # First registration
    client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'username': 'testuser',
        'password': 'Test1234'
    })
    
    # Second registration with same email
    response = client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'username': 'testuser2',
        'password': 'Test1234'
    })
    
    assert response.status_code == 409


def test_login_success(client):
    """Test successful login"""
    # Register user
    client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'username': 'testuser',
        'password': 'Test1234'
    })
    
    # Login
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'Test1234'
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'access_token' in data


def test_login_invalid_credentials(client):
    """Test login with invalid credentials"""
    response = client.post('/api/auth/login', json={
        'username': 'nonexistent',
        'password': 'wrongpass'
    })
    
    assert response.status_code == 401
