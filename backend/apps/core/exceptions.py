"""
Custom exception handler for consistent API error responses.

This demonstrates error handling best practices:
- Consistent error response format
- Proper HTTP status codes
- Detailed error messages for debugging
- User-friendly error messages
"""

from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    """
    Custom exception handler that formats all errors consistently.
    
    Returns:
        Response with format:
        {
            "error": "Error message",
            "detail": "Detailed error information",
            "status_code": 400
        }
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    if response is not None:
        custom_response_data = {
            'error': True,
            'message': str(exc),
            'status_code': response.status_code
        }
        
        # Add detailed errors if available
        if hasattr(response, 'data'):
            custom_response_data['details'] = response.data
        
        response.data = custom_response_data
    
    return response
