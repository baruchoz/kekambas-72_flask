from app import app, db
from app.models import Post
from app.blueprints.auth.models import User

if __name__ == '__main__':
    app.run()


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Post': Post
    }