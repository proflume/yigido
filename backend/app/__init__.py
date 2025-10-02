"""
Flask Application Factory
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_socketio import SocketIO
from redis import Redis
import os

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
socketio = SocketIO()
redis_client = None


def create_app(config_name=None):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Configuration
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app.config.update(
        # Database
        SQLALCHEMY_DATABASE_URI=os.getenv(
            'DATABASE_URL',
            'postgresql://postgres:postgres@localhost:5432/fullstack_app'
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        
        # Security
        SECRET_KEY=os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production'),
        JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production'),
        JWT_ACCESS_TOKEN_EXPIRES=3600,  # 1 hour
        JWT_REFRESH_TOKEN_EXPIRES=2592000,  # 30 days
        
        # Redis
        REDIS_URL=os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
        
        # Upload
        MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16MB max file size
        UPLOAD_FOLDER=os.getenv('UPLOAD_FOLDER', '/tmp/uploads'),
    )
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    socketio.init_app(app, cors_allowed_origins="*")
    
    # Initialize Redis
    global redis_client
    redis_client = Redis.from_url(app.config['REDIS_URL'], decode_responses=True)
    
    # Register blueprints
    from app.routes import auth, users, tasks, analytics
    app.register_blueprint(auth.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(tasks.bp)
    app.register_blueprint(analytics.bp)
    
    # Error handlers
    from app.utils.error_handlers import register_error_handlers
    register_error_handlers(app)
    
    return app
