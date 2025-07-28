from .auth import bp as auth_bp
from .user import bp as user_bp
from .db_setup import bp as db_setup_bp
from .post import bp as post_bp
from .comment import bp as comment_bp
from .like import bp as like_bp
from .admin import bp as admin_bp
from .shop import bp as shop_bp
from .group import bp as group_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(db_setup_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(comment_bp)
    app.register_blueprint(like_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(shop_bp)
    app.register_blueprint(group_bp) 