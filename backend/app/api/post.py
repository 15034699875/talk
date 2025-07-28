from flask import Blueprint, request, jsonify
from ..models.post import Post
from ..models.user import User
from .. import db
from ..utils.jwt import verify_jwt
from ..services.points import add_points, POINT_RULES

bp = Blueprint('post', __name__, url_prefix='/api/post')

@bp.route('', methods=['GET'])
def list_posts():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return jsonify([
        {
            'id': p.id,
            'title': p.title,
            'summary': p.content[:80] + ('...' if len(p.content) > 80 else ''),
            'author': p.author.username if p.author else '',
            'created_at': p.created_at.strftime('%Y-%m-%d %H:%M')
        } for p in posts
    ])

@bp.route('', methods=['POST'])
def create_post():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    payload = verify_jwt(token)
    if not payload:
        return jsonify({'msg': '未登录'}), 401
    data = request.json
    title = data.get('title')
    content = data.get('content')
    if not title or not content:
        return jsonify({'msg': '标题和内容不能为空'}), 400
    post = Post(title=title, content=content, author_id=payload['user_id'])
    db.session.add(post)
    db.session.commit()
    # 发帖加积分
    user = User.query.get(payload['user_id'])
    add_points(user, POINT_RULES['post'], '发帖')
    return jsonify({'msg': '发布成功', 'id': post.id}) 