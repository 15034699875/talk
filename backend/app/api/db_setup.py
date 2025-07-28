from flask import Blueprint, request, jsonify
from ..db_config import get_db_config, save_db_config
from sqlalchemy import create_engine, text
import os
from .. import db
from .. import create_app

bp = Blueprint('db_setup', __name__, url_prefix='/api/db')

@bp.route('/status', methods=['GET'])
def db_status():
    config = get_db_config()
    return jsonify({'initialized': bool(config)})

@bp.route('/init', methods=['POST'])
def db_init():
    # 防止重复初始化
    if get_db_config():
        return jsonify({'msg': '数据库已初始化，请勿重复操作', 'success': False}), 400
    data = request.json
    host = data.get('host')
    port = data.get('port')
    user = data.get('user')
    password = data.get('password')
    database = data.get('database')
    if not all([host, port, user, password, database]):
        return jsonify({'msg': '参数不完整'}), 400
    url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    try:
        engine = create_engine(url)
        # 创建数据库（如未存在）
        with engine.connect() as conn:
            conn.execute(text('CREATE DATABASE IF NOT EXISTS `%s` DEFAULT CHARSET utf8mb4' % database))
        # 保存配置
        save_db_config({'host': host, 'port': port, 'user': user, 'password': password, 'database': database})
        # 自动建表
        app = create_app()
        with app.app_context():
            db.create_all()
        return jsonify({'msg': '数据库连接成功并已初始化表结构', 'success': True})
    except Exception as e:
        return jsonify({'msg': f'数据库连接失败: {str(e)}', 'success': False}), 500 