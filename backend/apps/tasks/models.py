"""
Task Models

This demonstrates Django model design best practices:
- Proper field types and constraints
- Relationships (ForeignKey, ManyToMany)
- Choices for status and priority
- Meta options for ordering and indexes
- Custom methods and properties
- Timestamps for audit trail
"""

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    """Task category for organization."""
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#3B82F6', help_text='Hex color code')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Task(models.Model):
    """
    Task Model
    
    Represents a task with various attributes:
    - Priority levels (Low, Medium, High, Urgent)
    - Status tracking (Todo, In Progress, Done)
    - Due dates
    - Categorization
    - User assignment
    """
    
    # Priority choices
    class Priority(models.TextChoices):
        LOW = 'low', _('Low')
        MEDIUM = 'medium', _('Medium')
        HIGH = 'high', _('High')
        URGENT = 'urgent', _('Urgent')
    
    # Status choices
    class Status(models.TextChoices):
        TODO = 'todo', _('To Do')
        IN_PROGRESS = 'in_progress', _('In Progress')
        DONE = 'done', _('Done')
    
    # Core fields
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    # Status and priority
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.TODO
    )
    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM
    )
    
    # Relationships
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks'
    )
    
    # Dates
    due_date = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('task')
        verbose_name_plural = _('tasks')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['due_date']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return self.title
    
    @property
    def is_overdue(self):
        """Check if task is overdue."""
        if self.due_date and self.status != self.Status.DONE:
            from django.utils import timezone
            return timezone.now() > self.due_date
        return False


class Comment(models.Model):
    """Comments on tasks for collaboration."""
    
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Comment by {self.user} on {self.task}'
