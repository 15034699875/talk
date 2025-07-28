from flask import Blueprint, request, jsonify
from ..models.group import Group, GroupMember
from ..models.user import User
from .. import db
from ..utils.jwt import verify_jwt

bp = Blueprint('group', __name__, url_prefix='/api/group')

@bp.route('', methods=['POST'])
def create_group():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    payload = verify_jwt(token)
    if not payload:
        return jsonify({'msg': '未登录'}), 401
    data = request.json
    name = data.get('name')
    if not name:
        return jsonify({'msg': '群组名不能为空'}), 400
    group = Group(name=name, owner_id=payload['user_id'])
    db.session.add(group)
    db.session.commit()
    # 自动将创建者加入为群主
    db.session.add(GroupMember(user_id=payload['user_id'], group_id=group.id, role='owner'))
    db.session.commit()
    return jsonify({'msg': '创建成功', 'id': group.id})

@bp.route('/search', methods=['GET'])
def search_group():
    q = request.args.get('q', '')
    groups = Group.query.filter(Group.name.like(f'%{q}%')).all()
    return jsonify([
        {'id': g.id, 'name': g.name, 'owner_id': g.owner_id}
        for g in groups
    ])

@bp.route('/<int:group_id>/join', methods=['POST'])
def join_group(group_id):
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    payload = verify_jwt(token)
    if not payload:
        return jsonify({'msg': '未登录'}), 401
    # 检查是否已加入
    if GroupMember.query.filter_by(user_id=payload['user_id'], group_id=group_id).first():
        return jsonify({'msg': '已加入该群'}), 400
    db.session.add(GroupMember(user_id=payload['user_id'], group_id=group_id, role='member'))
    db.session.commit()
    return jsonify({'msg': '加入成功'})

@bp.route('/<int:group_id>/members', methods=['GET'])
def group_members(group_id):
    members = GroupMember.query.filter_by(group_id=group_id).all()
    return jsonify([
        {'user_id': m.user_id, 'role': m.role}
        for m in members
    ])

@bp.route('/<int:group_id>/set_role', methods=['POST'])
def set_member_role(group_id):
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    payload = verify_jwt(token)
    if not payload:
        return jsonify({'msg': '未登录'}), 401
    data = request.json
    user_id = data.get('user_id')
    role = data.get('role')
    # 只有群主可操作
    group = Group.query.get(group_id)
    if not group or group.owner_id != payload['user_id']:
        return jsonify({'msg': '无权限'}), 403
    member = GroupMember.query.filter_by(user_id=user_id, group_id=group_id).first()
    if not member:
        return jsonify({'msg': '成员不存在'}), 404
    member.role = role
    db.session.commit()
    return jsonify({'msg': '角色已更新'}) 