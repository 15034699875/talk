from .. import db
import datetime

class ShopOrder(db.Model):
    __tablename__ = 'shop_orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('shop_items.id'))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    status = db.Column(db.String(20), default='success')  # success/failed
    user = db.relationship('User', backref='shop_orders')
    item = db.relationship('ShopItem', backref='orders') 