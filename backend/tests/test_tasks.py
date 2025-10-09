"""
Task API Tests

Testing task CRUD operations and custom endpoints.
"""

import pytest
from rest_framework import status
from apps.tasks.models import Task, Comment


@pytest.mark.django_db
class TestTaskCRUD:
    """Test task CRUD operations."""
    
    def test_list_tasks(self, authenticated_client, task):
        """Test listing tasks."""
        response = authenticated_client.get('/api/v1/tasks/')
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['title'] == task.title
    
    def test_create_task(self, authenticated_client, category):
        """Test creating a task."""
        payload = {
            'title': 'New Task',
            'description': 'Task description',
            'status': Task.Status.TODO,
            'priority': Task.Priority.HIGH,
            'category': category.id
        }
        
        response = authenticated_client.post('/api/v1/tasks/', payload)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == payload['title']
        
        # Verify database
        task = Task.objects.get(id=response.data['id'])
        assert task.title == payload['title']
        assert task.category == category
    
    def test_retrieve_task(self, authenticated_client, task):
        """Test retrieving a single task."""
        response = authenticated_client.get(f'/api/v1/tasks/{task.id}/')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == task.title
        assert response.data['user']['email'] == task.user.email
    
    def test_update_task(self, authenticated_client, task):
        """Test updating a task."""
        payload = {
            'title': 'Updated Task',
            'status': Task.Status.IN_PROGRESS
        }
        
        response = authenticated_client.patch(f'/api/v1/tasks/{task.id}/', payload)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == payload['title']
        
        task.refresh_from_db()
        assert task.title == payload['title']
    
    def test_delete_task(self, authenticated_client, task):
        """Test deleting a task."""
        task_id = task.id
        response = authenticated_client.delete(f'/api/v1/tasks/{task_id}/')
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Task.objects.filter(id=task_id).exists()
    
    def test_user_can_only_see_own_tasks(self, api_client, user, task):
        """Test that users can only see their own tasks."""
        # Create another user
        from django.contrib.auth import get_user_model
        User = get_user_model()
        other_user = User.objects.create_user(
            email='other@example.com',
            password='pass123'
        )
        
        # Authenticate as other user
        api_client.force_authenticate(user=other_user)
        
        response = api_client.get('/api/v1/tasks/')
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 0


@pytest.mark.django_db
class TestTaskFiltering:
    """Test task filtering and search."""
    
    def test_filter_by_status(self, authenticated_client, user):
        """Test filtering tasks by status."""
        Task.objects.create(
            title='Todo Task',
            user=user,
            status=Task.Status.TODO
        )
        Task.objects.create(
            title='Done Task',
            user=user,
            status=Task.Status.DONE
        )
        
        response = authenticated_client.get('/api/v1/tasks/?status=todo')
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['status'] == Task.Status.TODO
    
    def test_search_tasks(self, authenticated_client, user):
        """Test searching tasks by title."""
        Task.objects.create(title='Important Task', user=user)
        Task.objects.create(title='Regular Task', user=user)
        
        response = authenticated_client.get('/api/v1/tasks/?search=Important')
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert 'Important' in response.data['results'][0]['title']


@pytest.mark.django_db
class TestTaskStatistics:
    """Test task statistics endpoint."""
    
    def test_statistics(self, authenticated_client, user):
        """Test getting task statistics."""
        # Create various tasks
        Task.objects.create(title='Task 1', user=user, status=Task.Status.TODO)
        Task.objects.create(title='Task 2', user=user, status=Task.Status.TODO)
        Task.objects.create(title='Task 3', user=user, status=Task.Status.DONE)
        
        response = authenticated_client.get('/api/v1/tasks/statistics/')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['total'] == 3
        assert response.data['by_status']['todo'] == 2
        assert response.data['by_status']['done'] == 1


@pytest.mark.django_db
class TestComments:
    """Test task comments."""
    
    def test_add_comment(self, authenticated_client, task):
        """Test adding a comment to a task."""
        payload = {'text': 'This is a comment'}
        
        response = authenticated_client.post(
            f'/api/v1/tasks/{task.id}/add_comment/',
            payload
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['text'] == payload['text']
        
        # Verify database
        comment = Comment.objects.get(id=response.data['id'])
        assert comment.task == task
        assert comment.text == payload['text']
