"""
Error handlers
"""
from flask import jsonify
from werkzeug.exceptions import HTTPException
from flask_jwt_extended.exceptions import JWTExtendedException


def register_error_handlers(app):
    """Register error handlers for the application"""
    
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({'error': 'Bad request', 'message': str(e)}), 400
    
    @app.errorhandler(401)
    def unauthorized(e):
        return jsonify({'error': 'Unauthorized', 'message': str(e)}), 401
    
    @app.errorhandler(403)
    def forbidden(e):
        return jsonify({'error': 'Forbidden', 'message': str(e)}), 403
    
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'error': 'Not found', 'message': str(e)}), 404
    
    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return jsonify({'error': e.name, 'message': e.description}), e.code
    
    @app.errorhandler(JWTExtendedException)
    def handle_jwt_exception(e):
        return jsonify({'error': 'JWT error', 'message': str(e)}), 401
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.error(f'Unhandled exception: {str(e)}')
        return jsonify({'error': 'Internal server error', 'message': 'An unexpected error occurred'}), 500
