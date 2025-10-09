"""
Task Serializers

This demonstrates serializer best practices:
- Nested serializers for relationships
- Custom field representations
- Validation logic
- Different serializers for list vs detail views
"""

from rest_framework import serializers
from .models import Task, Category, Comment
from apps.users.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for task categories."""
    
    task_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'color', 'task_count', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')
    
    def get_task_count(self, obj):
        """Get count of tasks in this category."""
        return obj.tasks.count()


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for task comments."""
    
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = ('id', 'task', 'user', 'text', 'created_at', 'updated_at')
        read_only_fields = ('task', 'user', 'created_at', 'updated_at')


class TaskListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for task lists."""
    
    category_name = serializers.CharField(source='category.name', read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Task
        fields = (
            'id', 'title', 'status', 'priority', 'category_name',
            'due_date', 'is_overdue', 'created_at', 'updated_at'
        )


class TaskDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for individual tasks."""
    
    user = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        required=False,
        allow_null=True
    )
    comments = CommentSerializer(many=True, read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Task
        fields = (
            'id', 'title', 'description', 'status', 'priority',
            'user', 'category', 'category_id', 'due_date', 'completed_at',
            'is_overdue', 'comments', 'created_at', 'updated_at'
        )
        read_only_fields = ('user', 'completed_at', 'created_at', 'updated_at')
    
    def update(self, instance, validated_data):
        """Auto-set completed_at when status changes to done."""
        if validated_data.get('status') == Task.Status.DONE and instance.status != Task.Status.DONE:
            from django.utils import timezone
            validated_data['completed_at'] = timezone.now()
        elif validated_data.get('status') != Task.Status.DONE:
            validated_data['completed_at'] = None
        
        return super().update(instance, validated_data)


class TaskCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating tasks."""
    
    class Meta:
        model = Task
        fields = ('title', 'description', 'status', 'priority', 'category', 'due_date')
