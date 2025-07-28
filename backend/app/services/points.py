from ..models.user import User
from ..models.point_log import PointLog
from .. import db

# 积分与经验累加函数
# user: 用户对象，amount: 积分变动值，reason: 变动原因（如发帖、评论等）
def add_points(user: User, amount: int, reason: str):
    # 增加用户积分
    user.points += amount
    # 经验值 = 积分 * 2
    user.exp = user.points * 2
    # 记录积分变动日志，便于审计和追踪
    db.session.add(PointLog(user_id=user.id, change=amount, reason=reason))
    # 提交数据库事务
    db.session.commit()

# 根据经验值计算等级，每1000经验升一级
# exp: 经验值，返回等级（int）
def get_level(exp: int) -> int:
    return exp // 1000 + 1

# 业务积分规则定义
# 不同行为对应不同积分奖励
POINT_RULES = {
    'post': 5,        # 发帖+5分
    'comment': 2,     # 评论+2分
    'post_like': 3,   # 帖子被赞+3分
    'comment_like': 1 # 评论被赞+1分
} 