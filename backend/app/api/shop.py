from flask import Blueprint, request, jsonify
from ..models.shop_item import ShopItem
from ..models.shop_order import ShopOrder
from ..models.user import User
from .. import db
from ..utils.jwt import verify_jwt
from ..services.points import add_points

bp = Blueprint('shop', __name__, url_prefix='/api/shop')

@bp.route('/items', methods=['GET'])
def list_items():
    items = ShopItem.query.filter(ShopItem.stock > 0).all()
    return jsonify([
        {'id': i.id, 'name': i.name, 'description': i.description, 'points': i.points, 'stock': i.stock, 'type': i.type, 'download_url': i.download_url}
        for i in items
    ])

@bp.route('/order', methods=['POST'])
def order_item():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    payload = verify_jwt(token)
    if not payload:
        return jsonify({'msg': '未登录'}), 401
    user = User.query.get(payload['user_id'])
    data = request.json
    item_id = data.get('item_id')
    item = ShopItem.query.get(item_id)
    if not item or item.stock <= 0:
        return jsonify({'msg': '商品不存在或已售罄'}), 400
    if user.points < item.points:
        return jsonify({'msg': '积分不足'}), 400
    # 扣除积分，减少库存，生成订单
    user.points -= item.points
    user.exp = user.points * 2
    item.stock -= 1
    order = ShopOrder(user_id=user.id, item_id=item.id)
    db.session.add(order)
    db.session.commit()
    return jsonify({'msg': '兑换成功', 'order_id': order.id, 'download_url': item.download_url})

@bp.route('/orders', methods=['GET'])
def my_orders():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    payload = verify_jwt(token)
    if not payload:
        return jsonify({'msg': '未登录'}), 401
    orders = ShopOrder.query.filter_by(user_id=payload['user_id']).order_by(ShopOrder.created_at.desc()).all()
    return jsonify([
        {'id': o.id, 'item_name': o.item.name, 'created_at': o.created_at.strftime('%Y-%m-%d %H:%M'), 'status': o.status, 'download_url': o.item.download_url}
        for o in orders
    ]) 