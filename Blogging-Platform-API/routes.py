# routes.py
from flask import Blueprint, request, jsonify
from models import db, Post

blog_routes = Blueprint('blog_routes', __name__)

@blog_routes.route('/blog/new', methods=['POST'])
def create_blog_post():
    data = request.json
    if not all(key in data for key in ('title', 'content', 'category')):
        return jsonify({'error': 'Missing required fields'}), 400
    
    new_post = Post(
        title=data['title'],
        content=data['content'],
        category=data['category'],
        tags=','.join(data.get('tags', []))
    )
    db.session.add(new_post)
    db.session.commit()
    return jsonify(new_post.to_dict()), 201

@blog_routes.route('/blog/edit/<int:post_id>', methods=['PUT'])
def update_blog_post(post_id):
    post = Post.query.get_or_404(post_id)
    data = request.json
    post.title = data.get('title', post.title)
    post.content = data.get('content', post.content)
    post.category = data.get('category', post.category)
    post.tags = ','.join(data.get('tags', post.tags.split(',') if post.tags else []))
    db.session.commit()
    return jsonify(post.to_dict()), 200

@blog_routes.route('/blog/remove/<int:post_id>', methods=['DELETE'])
def delete_blog_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return '', 204

@blog_routes.route('/blog/view/<int:post_id>', methods=['GET'])
def get_single_blog_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify(post.to_dict()), 200

@blog_routes.route('/blog/list', methods=['GET'])
def list_blog_posts():
    term = request.args.get('term')
    if term:
        posts = Post.query.filter(
            (Post.title.ilike(f'%{term}%')) |
            (Post.content.ilike(f'%{term}%')) |
            (Post.category.ilike(f'%{term}%'))
        ).all()
    else:
        posts = Post.query.all()
    return jsonify([post.to_dict() for post in posts]), 200