from . import create_app, socketio

# 导入chat事件，注册SocketIO事件处理器
from .api import chat

app = create_app()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000) 