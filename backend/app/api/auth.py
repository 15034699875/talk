from flask import Blueprint, request, jsonify
from ..models.user import User
from .. import db
from ..utils.bcrypt import hash_password, check_password
from ..utils.jwt import generate_jwt

bp = Blueprint('auth', __name__, url_prefix='/api')

@bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    if not username or not password or not email:
        return jsonify({'msg': '缺少参数'}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({'msg': '用户名已存在'}), 409
    user = User(username=username, password_hash=hash_password(password), email=email)
    db.session.add(user)
    db.session.commit()
    return jsonify({'msg': '注册成功'})

@bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if not user or not check_password(password, user.password_hash):
        return jsonify({'msg': '用户名或密码错误'}), 401
    if user.is_banned:
        return jsonify({'msg': '账号已被封禁'}), 403
    token = generate_jwt(user.id, user.role)
    return jsonify({'token': token, 'user': {'id': user.id, 'username': user.username, 'role': user.role}}) 