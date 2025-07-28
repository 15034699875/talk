from flask import request
from flask_socketio import emit, join_room, leave_room
from .. import socketio, db
from ..models.user import User
from ..models.group import Group, GroupMember
import datetime

# 简单内存离线消息存储（生产建议用Redis等持久化）
offline_messages = {}

@socketio.on('private_message')
def handle_private_message(data):
    sender_id = data.get('sender_id')
    receiver_id = data.get('receiver_id')
    content = data.get('content')
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M')
    msg = {'from': sender_id, 'to': receiver_id, 'content': content, 'timestamp': timestamp}
    room = f'user_{receiver_id}'
    emit('private_message', msg, room=room)
    # 离线存储
    offline_messages.setdefault(receiver_id, []).append(msg)

@socketio.on('join_user')
def join_user(data):
    user_id = data.get('user_id')
    join_room(f'user_{user_id}')
    # 发送离线消息
    msgs = offline_messages.get(user_id, [])
    for m in msgs:
        emit('private_message', m)
    offline_messages[user_id] = []

@socketio.on('group_message')
def handle_group_message(data):
    sender_id = data.get('sender_id')
    group_id = data.get('group_id')
    content = data.get('content')
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M')
    msg = {'from': sender_id, 'group_id': group_id, 'content': content, 'timestamp': timestamp}
    room = f'group_{group_id}'
    emit('group_message', msg, room=room)

@socketio.on('join_group')
def join_group_socket(data):
    group_id = data.get('group_id')
    join_room(f'group_{group_id}') 