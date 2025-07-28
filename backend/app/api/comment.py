from flask import Blueprint, request, jsonify
from ..models.comment import Comment
from ..models.user import User
from ..models.post import Post
from .. import db
from ..utils.jwt import verify_jwt
from ..services.points import add_points, POINT_RULES

bp = Blueprint('comment', __name__, url_prefix='/api/comment')

@bp.route('/<int:post_id>', methods=['GET'])
def list_comments(post_id):
    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.created_at.asc()).all()
    return jsonify([
        {
            'id': c.id,
            'content': c.content,
            'author': c.author.username if c.author else '',
            'created_at': c.created_at.strftime('%Y-%m-%d %H:%M')
        } for c in comments
    ])

@bp.route('/<int:post_id>', methods=['POST'])
def create_comment(post_id):
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    payload = verify_jwt(token)
    if not payload:
        return jsonify({'msg': '未登录'}), 401
    data = request.json
    content = data.get('content')
    if not content:
        return jsonify({'msg': '内容不能为空'}), 400
    comment = Comment(content=content, author_id=payload['user_id'], post_id=post_id)
    db.session.add(comment)
    db.session.commit()
    # 评论加积分
    user = User.query.get(payload['user_id'])
    add_points(user, POINT_RULES['comment'], '评论')
    return jsonify({'msg': '评论成功', 'id': comment.id}) 