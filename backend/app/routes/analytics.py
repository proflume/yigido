"""
Analytics Routes
"""
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db, redis_client
from app.models import Task
from sqlalchemy import func
from datetime import datetime, timedelta
import json

bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')


@bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    """Get dashboard statistics"""
    user_id = get_jwt_identity()
    
    # Check cache
    cache_key = f'analytics:dashboard:{user_id}'
    cached = redis_client.get(cache_key)
    if cached:
        return jsonify(json.loads(cached)), 200
    
    # Task counts by status
    status_counts = db.session.query(
        Task.status, func.count(Task.id)
    ).filter_by(user_id=user_id).group_by(Task.status).all()
    
    # Task counts by priority
    priority_counts = db.session.query(
        Task.priority, func.count(Task.id)
    ).filter_by(user_id=user_id).group_by(Task.priority).all()
    
    # Tasks completed this week
    week_ago = datetime.utcnow() - timedelta(days=7)
    completed_this_week = Task.query.filter(
        Task.user_id == user_id,
        Task.status == 'completed',
        Task.completed_at >= week_ago
    ).count()
    
    # Overdue tasks
    overdue_tasks = Task.query.filter(
        Task.user_id == user_id,
        Task.status != 'completed',
        Task.due_date < datetime.utcnow()
    ).count()
    
    # Total tasks
    total_tasks = Task.query.filter_by(user_id=user_id).count()
    
    stats = {
        'total_tasks': total_tasks,
        'completed_this_week': completed_this_week,
        'overdue_tasks': overdue_tasks,
        'status_distribution': {status: count for status, count in status_counts},
        'priority_distribution': {priority: count for priority, count in priority_counts}
    }
    
    # Cache for 5 minutes
    redis_client.setex(cache_key, 300, json.dumps(stats))
    
    return jsonify(stats), 200


@bp.route('/productivity', methods=['GET'])
@jwt_required()
def get_productivity_stats():
    """Get productivity statistics over time"""
    user_id = get_jwt_identity()
    
    # Last 30 days of completed tasks
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    daily_completed = db.session.query(
        func.date(Task.completed_at).label('date'),
        func.count(Task.id).label('count')
    ).filter(
        Task.user_id == user_id,
        Task.status == 'completed',
        Task.completed_at >= thirty_days_ago
    ).group_by(func.date(Task.completed_at)).all()
    
    return jsonify({
        'daily_completed': [
            {'date': str(date), 'count': count}
            for date, count in daily_completed
        ]
    }), 200
