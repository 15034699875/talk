# 导入所有模型，便于db.create_all()
from .user import User
from .group import Group, GroupMember
from .point_log import PointLog
from .post import Post
from .comment import Comment
from .like import Like
from .shop_item import ShopItem
from .shop_order import ShopOrder 