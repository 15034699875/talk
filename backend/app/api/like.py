from flask import Blueprint, request, jsonify
from ..models.like import Like
from ..models.post import Post
from ..models.comment import Comment
from ..models.user import User
from .. import db
from ..utils.jwt import verify_jwt
from ..services.points import add_points, POINT_RULES

bp = Blueprint('like', __name__, url_prefix='/api/like')

@bp.route('', methods=['POST'])
def like():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    payload = verify_jwt(token)
    if not payload:
        return jsonify({'msg': '未登录'}), 401
    data = request.json
    target_type = data.get('target_type')  # 'post' or 'comment'
    target_id = data.get('target_id')
    if target_type not in ('post', 'comment') or not target_id:
        return jsonify({'msg': '参数错误'}), 400
    # 检查是否已点赞
    like = Like.query.filter_by(user_id=payload['user_id'], target_type=target_type, target_id=target_id).first()
    if like:
        db.session.delete(like)
        db.session.commit()
        action = 'unlike'
    else:
        db.session.add(Like(user_id=payload['user_id'], target_type=target_type, target_id=target_id))
        db.session.commit()
        action = 'like'
        # 被点赞加分
        if target_type == 'post':
            post = Post.query.get(target_id)
            if post and post.author_id != payload['user_id']:
                user = User.query.get(post.author_id)
                add_points(user, POINT_RULES['post_like'], '帖子被赞')
        elif target_type == 'comment':
            comment = Comment.query.get(target_id)
            if comment and comment.author_id != payload['user_id']:
                user = User.query.get(comment.author_id)
                add_points(user, POINT_RULES['comment_like'], '评论被赞')
    # 统计点赞数
    count = Like.query.filter_by(target_type=target_type, target_id=target_id).count()
    return jsonify({'msg': '操作成功', 'action': action, 'count': count})

@bp.route('/count', methods=['GET'])
def like_count():
    target_type = request.args.get('target_type')
    target_id = request.args.get('target_id')
    if target_type not in ('post', 'comment') or not target_id:
        return jsonify({'count': 0})
    count = Like.query.filter_by(target_type=target_type, target_id=target_id).count()
    return jsonify({'count': count}) 