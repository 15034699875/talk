from flask import Blueprint, request, jsonify
from ..models.post import Post
from ..models.comment import Comment
from ..models.user import User
from ..models.point_log import PointLog
from .. import db
from ..utils.jwt import verify_jwt
from ..services.points import add_points

bp = Blueprint('admin', __name__, url_prefix='/api/admin')

def admin_required():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    payload = verify_jwt(token)
    if not payload or payload.get('role') != 'admin':
        return None
    return payload

@bp.route('/posts', methods=['GET'])
def admin_list_posts():
    if not admin_required():
        return jsonify({'msg': '无权限'}), 403
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return jsonify([
        {'id': p.id, 'title': p.title, 'author': p.author.username if p.author else '', 'created_at': p.created_at.strftime('%Y-%m-%d %H:%M')}
        for p in posts
    ])

@bp.route('/posts/<int:post_id>', methods=['DELETE'])
def admin_delete_post(post_id):
    if not admin_required():
        return jsonify({'msg': '无权限'}), 403
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'msg': '帖子不存在'}), 404
    db.session.delete(post)
    db.session.commit()
    return jsonify({'msg': '删除成功'})

@bp.route('/comments', methods=['GET'])
def admin_list_comments():
    if not admin_required():
        return jsonify({'msg': '无权限'}), 403
    comments = Comment.query.order_by(Comment.created_at.desc()).all()
    return jsonify([
        {'id': c.id, 'content': c.content, 'author': c.author.username if c.author else '', 'post_id': c.post_id, 'created_at': c.created_at.strftime('%Y-%m-%d %H:%M')}
        for c in comments
    ])

@bp.route('/comments/<int:comment_id>', methods=['DELETE'])
def admin_delete_comment(comment_id):
    if not admin_required():
        return jsonify({'msg': '无权限'}), 403
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({'msg': '评论不存在'}), 404
    db.session.delete(comment)
    db.session.commit()
    return jsonify({'msg': '删除成功'})

@bp.route('/users/<int:user_id>/ban', methods=['POST'])
def admin_ban_user(user_id):
    if not admin_required():
        return jsonify({'msg': '无权限'}), 403
    user = User.query.get(user_id)
    if not user:
        return jsonify({'msg': '用户不存在'}), 404
    user.is_banned = True
    db.session.commit()
    return jsonify({'msg': '已封禁'})

@bp.route('/users/<int:user_id>/points', methods=['POST'])
def admin_add_points(user_id):
    if not admin_required():
        return jsonify({'msg': '无权限'}), 403
    user = User.query.get(user_id)
    if not user:
        return jsonify({'msg': '用户不存在'}), 404
    data = request.json
    amount = data.get('amount')
    reason = data.get('reason', '管理员操作')
    try:
        amount = int(amount)
    except:
        return jsonify({'msg': '积分必须为整数'}), 400
    add_points(user, amount, reason)
    return jsonify({'msg': '操作成功'})

@bp.route('/points/logs', methods=['GET'])
def admin_point_logs():
    if not admin_required():
        return jsonify({'msg': '无权限'}), 403
    logs = PointLog.query.order_by(PointLog.created_at.desc()).all()
    return jsonify([
        {'id': l.id, 'user_id': l.user_id, 'change': l.change, 'reason': l.reason, 'created_at': l.created_at.strftime('%Y-%m-%d %H:%M')}
        for l in logs
    ]) 