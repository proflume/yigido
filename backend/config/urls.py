"""
URL Configuration for Task Manager API

This demonstrates RESTful API URL design best practices:
- Versioned API endpoints (/api/v1/)
- Logical resource grouping
- Clear, descriptive URL patterns
- Separation of concerns
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.admin),
    
    # API v1
    path('api/v1/auth/', include('apps.users.urls')),
    path('api/v1/tasks/', include('apps.tasks.urls')),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
