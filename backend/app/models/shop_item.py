from .. import db

class ShopItem(db.Model):
    __tablename__ = 'shop_items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    points = db.Column(db.Integer, nullable=False)  # 兑换所需积分
    stock = db.Column(db.Integer, default=0)        # 库存
    type = db.Column(db.String(50))                 # 商品类型（如代码模板、电子书等）
    download_url = db.Column(db.String(255))        # 下载链接（如有） 