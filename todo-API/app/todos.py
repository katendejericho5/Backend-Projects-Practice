from flask import Blueprint, request, jsonify
from app import db, limiter
from app.models import Todo
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('todos', __name__)

@bp.route('/todos', methods=['POST'])
@jwt_required()
@limiter.limit("10 per minute")
def create_todo():
    data = request.get_json()
    user_id = get_jwt_identity()
    todo = Todo(title=data['title'], description=data['description'], user_id=user_id)
    db.session.add(todo)
    db.session.commit()
    return jsonify({"id": todo.id, "title": todo.title, "description": todo.description}), 201

@bp.route('/todos', methods=['GET'])
@jwt_required()
def get_todos():
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    limit = min(request.args.get('limit', 10, type=int), 100)  # max 100 items per page
    query = Todo.query.filter_by(user_id=user_id)
    
    if 'title' in request.args:
        query = query.filter(Todo.title.ilike(f"%{request.args['title']}%"))
    if 'description' in request.args:
        query = query.filter(Todo.description.ilike(f"%{request.args['description']}%"))
    
    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    todos = pagination.items
    return jsonify({
        "data": [{"id": todo.id, "title": todo.title, "description": todo.description} for todo in todos],
        "page": page,
        "limit": limit,
        "total": pagination.total
    })

@bp.route('/todos/<int:id>', methods=['PUT'])
@jwt_required()
def update_todo(id):
    user_id = get_jwt_identity()
    todo = Todo.query.filter_by(id=id, user_id=user_id).first()
    if not todo:
        return jsonify({"message": "Todo not found or not authorized"}), 404
    data = request.get_json()
    todo.title = data.get('title', todo.title)
    todo.description = data.get('description', todo.description)
    db.session.commit()
    return jsonify({"id": todo.id, "title": todo.title, "description": todo.description})

@bp.route('/todos/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_todo(id):
    user_id = get_jwt_identity()
    todo = Todo.query.filter_by(id=id, user_id=user_id).first()
    if not todo:
        return jsonify({"message": "Todo not found or not authorized"}), 404
    db.session.delete(todo)
    db.session.commit()
    return '', 204