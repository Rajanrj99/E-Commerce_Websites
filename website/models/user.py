from website import db
from flask_login import UserMixin
class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(64),nullable=False,unique=True)
    password=db.Column(db.String(64),nullable=False)
    email=db.Column(db.String(64),nullable=False,unique=True)
    budget=db.Column(db.Integer,nullable=False,default=1000)
    item=db.relationship('Item',backref='owned_user',lazy=True)

    
    def can_purchase(self, item_obj):
        return self.budget >= item_obj.price
    
    def can_sell(self, item_obj):
        return item_obj in self.item

    