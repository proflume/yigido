"""
Task Admin Configuration

Customized Django admin for task management.
"""

from django.contrib import admin
from .models import Task, Category, Comment


class CommentInline(admin.TabularInline):
    """Inline comments in task detail page."""
    model = Comment
    extra = 0
    readonly_fields = ('created_at',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Admin interface for tasks."""
    
    list_display = ('title', 'user', 'status', 'priority', 'category', 'due_date', 'created_at')
    list_filter = ('status', 'priority', 'category', 'created_at')
    search_fields = ('title', 'description', 'user__email')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    inlines = [CommentInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'user')
        }),
        ('Classification', {
            'fields': ('status', 'priority', 'category')
        }),
        ('Dates', {
            'fields': ('due_date', 'completed_at', 'created_at', 'updated_at')
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for categories."""
    
    list_display = ('name', 'color', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin interface for comments."""
    
    list_display = ('task', 'user', 'text_preview', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('text', 'user__email', 'task__title')
    ordering = ('-created_at',)
    
    def text_preview(self, obj):
        """Show preview of comment text."""
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Comment'
