from flask import Blueprint, request, jsonify
from ..models.user import User
from ..models.point_log import PointLog
from ..utils.jwt import verify_jwt
from .. import db

bp = Blueprint('user', __name__, url_prefix='/api')

@bp.route('/user/profile', methods=['GET'])
def profile():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    payload = verify_jwt(token)
    if not payload:
        return jsonify({'msg': '无效token'}), 401
    user = User.query.get(payload['user_id'])
    if not user:
        return jsonify({'msg': '用户不存在'}), 404
    return jsonify({
        'id': user.id,
        'username': user.username,
        'avatar_url': user.avatar_url,
        'points': user.points,
        'exp': user.exp,
        'role': user.role,
        'email': user.email
    })

@bp.route('/user/profile', methods=['PUT'])
def update_profile():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    payload = verify_jwt(token)
    if not payload:
        return jsonify({'msg': '无效token'}), 401
    user = User.query.get(payload['user_id'])
    if not user:
        return jsonify({'msg': '用户不存在'}), 404
    data = request.json
    avatar_url = data.get('avatar_url')
    email = data.get('email')
    if avatar_url is not None:
        user.avatar_url = avatar_url
    if email is not None:
        user.email = email
    db.session.commit()
    return jsonify({'msg': '修改成功'})

@bp.route('/user/ban', methods=['POST'])
def ban_user():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    payload = verify_jwt(token)
    if not payload or payload.get('role') != 'admin':
        return jsonify({'msg': '无权限'}), 403
    data = request.json
    user_id = data.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return jsonify({'msg': '用户不存在'}), 404
    user.is_banned = True
    db.session.commit()
    return jsonify({'msg': '已封禁'})

# 新增：用户积分明细查询API
@bp.route('/user/points/logs', methods=['GET'])
def user_point_logs():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    payload = verify_jwt(token)
    if not payload:
        return jsonify({'msg': '无效token'}), 401
    logs = PointLog.query.filter_by(user_id=payload['user_id']).order_by(PointLog.created_at.desc()).all()
    return jsonify([
        {'id': l.id, 'change': l.change, 'reason': l.reason, 'created_at': l.created_at.strftime('%Y-%m-%d %H:%M')}
        for l in logs
    ]) 