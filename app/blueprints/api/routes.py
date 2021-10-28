from . import bp as api
from app.blueprints.auth.models import User
from app.blueprints.blog.models import Post
from flask import jsonify, request
from .auth import basic_auth


# Token Route

@api.route('/token', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = basic_auth.current_user().get_token()
    return jsonify({'token': token})


# User Routes

@api.route('/users')
def get_users():
    """
    [GET] /api/users - Returns all users
    """
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])


@api.route('/users/<id>')
def get_user(id):
    """
    [GET] /api/users/<id> - Return user based on id
    """
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict(True))


@api.route('/users', methods=['POST'])
def create_user():
    data = request.json
    for field in ['username', 'email', 'password']:
        if field not in data:
            return jsonify({'error': f'You are missing the {field} field'}), 400
    # Grab data from the request body
    username = data['username']
    email = data['email']
    password = data['password']

    # Check if the username from the form already exists in the User table
    existing_user = User.query.filter_by(username=username).all()
    # If there is a user with that username message them asking them to try again
    if existing_user:
        return jsonify({'error': f'The username {username} is already registered. Please try again.'}), 400

    # Create new user
    new_user = User(username, email, password)
    new_user.save()

    return jsonify(new_user.to_dict()), 201


@api.route('/users/<id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.json
    user.update_user(data)
    return jsonify(user.to_dict())


@api.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    user_to_delete = User.query.get_or_404(id)
    user_to_delete.delete()
    return jsonify({}), 204


# Blog Post routes

@api.route('/posts')
def get_posts():
    posts = Post.query.all()
    return jsonify([p.to_dict() for p in posts])


@api.route('/posts/<id>')
def get_post(id):
    """
    [GET] /api/posts/<id> - Return the post of url id
    """
    post = Post.query.get_or_404(id)
    return jsonify(post.to_dict())


@api.route('/posts', methods=['POST'])
def create_post():
    data = request.json
    for field in ['title', 'content', 'user_id']:
        if field not in data:
            return jsonify({'error': f'You are missing the {field} field'}), 400
    title = data['title']
    content = data['content']
    user_id = data['user_id']

    new_post = Post(title, content, user_id)
    new_post.save()
    return jsonify(new_post.to_dict()), 201


@api.route('/posts/<id>', methods=['PUT'])
def update_post(id):
    post_to_update = Post.query.get_or_404(id)
    update_data = request.json
    post_to_update.update_post(update_data)
    return jsonify(post_to_update.to_dict())


@api.route('/posts/<id>', methods=['DELETE'])
def delete_post(id):
    post_to_delete = Post.query.get_or_404(id)
    post_to_delete.delete()
    return jsonify({}), 204

