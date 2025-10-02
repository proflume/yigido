"""
Task Management Routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db, socketio
from app.models import Task, Tag
from datetime import datetime
from flask_socketio import emit

bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')


@bp.route('/', methods=['GET'])
@jwt_required()
def get_tasks():
    """Get all tasks for current user"""
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status')
    priority = request.args.get('priority')
    search = request.args.get('search', '')
    
    query = Task.query.filter_by(user_id=user_id)
    
    if status:
        query = query.filter_by(status=status)
    if priority:
        query = query.filter_by(priority=priority)
    if search:
        query = query.filter(Task.title.ilike(f'%{search}%'))
    
    pagination = query.order_by(Task.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'tasks': [task.to_dict() for task in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), 200


@bp.route('/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    """Get task by ID"""
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify({'task': task.to_dict()}), 200


@bp.route('/', methods=['POST'])
@jwt_required()
def create_task():
    """Create a new task"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or not data.get('title'):
        return jsonify({'error': 'Title is required'}), 400
    
    task = Task(
        title=data['title'],
        description=data.get('description', ''),
        status=data.get('status', 'pending'),
        priority=data.get('priority', 'medium'),
        user_id=user_id
    )
    
    # Handle due date
    if data.get('due_date'):
        try:
            task.due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Invalid due_date format'}), 400
    
    # Handle tags
    if data.get('tags'):
        for tag_name in data['tags']:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.session.add(tag)
            task.tags.append(tag)
    
    db.session.add(task)
    db.session.commit()
    
    # Emit WebSocket event
    socketio.emit('task_created', {'task': task.to_dict()}, room=f'user_{user_id}')
    
    return jsonify({
        'message': 'Task created successfully',
        'task': task.to_dict()
    }), 201


@bp.route('/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    """Update a task"""
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    data = request.get_json()
    
    # Update fields
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'status' in data:
        task.status = data['status']
        if data['status'] == 'completed' and not task.completed_at:
            task.completed_at = datetime.utcnow()
        elif data['status'] != 'completed':
            task.completed_at = None
    if 'priority' in data:
        task.priority = data['priority']
    if 'due_date' in data:
        if data['due_date']:
            try:
                task.due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
            except ValueError:
                return jsonify({'error': 'Invalid due_date format'}), 400
        else:
            task.due_date = None
    
    # Update tags
    if 'tags' in data:
        task.tags = []
        for tag_name in data['tags']:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.session.add(tag)
            task.tags.append(tag)
    
    db.session.commit()
    
    # Emit WebSocket event
    socketio.emit('task_updated', {'task': task.to_dict()}, room=f'user_{user_id}')
    
    return jsonify({
        'message': 'Task updated successfully',
        'task': task.to_dict()
    }), 200


@bp.route('/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    """Delete a task"""
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    db.session.delete(task)
    db.session.commit()
    
    # Emit WebSocket event
    socketio.emit('task_deleted', {'task_id': task_id}, room=f'user_{user_id}')
    
    return jsonify({'message': 'Task deleted successfully'}), 200


@bp.route('/tags', methods=['GET'])
@jwt_required()
def get_tags():
    """Get all tags"""
    tags = Tag.query.all()
    return jsonify({'tags': [tag.to_dict() for tag in tags]}), 200
