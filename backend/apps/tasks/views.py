"""
Task Views

This demonstrates advanced ViewSet patterns:
- Different serializers for list vs detail
- Filtering, searching, and ordering
- Custom actions
- Permission handling
- Optimized queries with select_related and prefetch_related
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Count
from django.utils import timezone

from .models import Task, Category, Comment
from .serializers import (
    TaskListSerializer,
    TaskDetailSerializer,
    TaskCreateSerializer,
    CategorySerializer,
    CommentSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for task categories.
    
    Provides CRUD operations for categories.
    """
    
    queryset = Category.objects.annotate(task_count=Count('tasks'))
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at', 'task_count']
    ordering = ['name']


class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for task management.
    
    Provides:
    - List tasks with filtering (GET /api/v1/tasks/)
    - Create task (POST /api/v1/tasks/)
    - Retrieve task detail (GET /api/v1/tasks/{id}/)
    - Update task (PUT/PATCH /api/v1/tasks/{id}/)
    - Delete task (DELETE /api/v1/tasks/{id}/)
    - Statistics (GET /api/v1/tasks/statistics/)
    - Overdue tasks (GET /api/v1/tasks/overdue/)
    """
    
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'due_date', 'priority']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """
        Optimize queries and filter by user.
        
        Demonstrates query optimization with select_related and prefetch_related.
        """
        queryset = Task.objects.filter(user=self.request.user).select_related(
            'user', 'category'
        ).prefetch_related('comments', 'comments__user')
        
        # Filter by status
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
        
        # Filter by priority
        priority = self.request.query_params.get('priority', None)
        if priority:
            queryset = queryset.filter(priority=priority)
        
        # Filter by category
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category_id=category)
        
        # Filter overdue tasks
        overdue = self.request.query_params.get('overdue', None)
        if overdue == 'true':
            queryset = queryset.filter(
                due_date__lt=timezone.now(),
                status__in=[Task.Status.TODO, Task.Status.IN_PROGRESS]
            )
        
        return queryset
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'list':
            return TaskListSerializer
        elif self.action == 'create':
            return TaskCreateSerializer
        return TaskDetailSerializer
    
    def perform_create(self, serializer):
        """Set the user when creating a task."""
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        Get task statistics for the current user.
        
        Returns counts by status, priority, and overdue tasks.
        """
        tasks = self.get_queryset()
        
        stats = {
            'total': tasks.count(),
            'by_status': {
                'todo': tasks.filter(status=Task.Status.TODO).count(),
                'in_progress': tasks.filter(status=Task.Status.IN_PROGRESS).count(),
                'done': tasks.filter(status=Task.Status.DONE).count(),
            },
            'by_priority': {
                'low': tasks.filter(priority=Task.Priority.LOW).count(),
                'medium': tasks.filter(priority=Task.Priority.MEDIUM).count(),
                'high': tasks.filter(priority=Task.Priority.HIGH).count(),
                'urgent': tasks.filter(priority=Task.Priority.URGENT).count(),
            },
            'overdue': tasks.filter(
                due_date__lt=timezone.now(),
                status__in=[Task.Status.TODO, Task.Status.IN_PROGRESS]
            ).count(),
        }
        
        return Response(stats)
    
    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """Get all overdue tasks."""
        tasks = self.get_queryset().filter(
            due_date__lt=timezone.now(),
            status__in=[Task.Status.TODO, Task.Status.IN_PROGRESS]
        )
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        """Add a comment to a task."""
        task = self.get_object()
        serializer = CommentSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(task=task, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet for managing comments."""
    
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter comments by user's tasks."""
        return Comment.objects.filter(
            task__user=self.request.user
        ).select_related('user', 'task')
    
    def perform_create(self, serializer):
        """Set the user when creating a comment."""
        serializer.save(user=self.request.user)
