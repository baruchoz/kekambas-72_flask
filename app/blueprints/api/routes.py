from . import bp as api
from app import db
from app.blueprints.auth.models import User
from app.blueprints.blog.models import Post
from flask import jsonify, request
from .auth import basic_auth


# Token Route

@api.route('/token', methods=['POST'])
@basic_auth.login_required
def get_token():
    print('GET TOKEN FUNCTION')
    
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
def get_users():
    """
    [GET] /api/posts - Returns all posts
    """
    posts = Post.query.all()
    return jsonify([post.to_dict() for post in posts])

@api.route('/posts/<id>')
def get_user(id):
    """
    [GET] /api/posts/<id> - Return posts based on id
    """
    post = Post.query.get_or_404(id)
    return jsonify(post.to_dict())

@api.route('/posts', methods=['POST'])
def create_posts():
    data = request.json
    for field in ['title', 'content']:
        if field not in data:
            return jsonify({'error': f'You are missing the {field} field'}), 400
    # Grab data from the request body
    title = data['title']
    content = data['content']

    # Check if the title from the already exists in the Post table
    existing_post = Post.query.filter_by(title=title).all()
    # If there is a post that has a Title taken, message them asking them to try again
    if existing_post:
        return jsonify({'error': f'The {title} of your post has been used already. Create a new Title.'}), 400

    # Create new post
    new_post = Post(title, content)
    new_post.save()

    return jsonify(new_post.to_dict())

@api.route('/posts/<id>', methods=['PUT'])
def update_post(id):
    post = Post.query.get_or_404(id)
    data = request.json
    post.update_post(data)
    return jsonify(post.to_dict())

@api.route('/posts/<id>', methods=['DELETE'])
def delete_post(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    
    return "Post was successfully deleted"