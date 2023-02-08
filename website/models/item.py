from website import db
class Item(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(30),nullable=False)
    price=db.Column(db.Float,nullable=False)
    barcode=db.Column(db.String(12),nullable=False,unique=True)
    description=db.Column(db.String(1024))
    owner=db.Column(db.Integer,db.ForeignKey('user.id'))
    
    def buy(self, user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()

    def sell(self, user):
        self.owner = None
        user.budget += self.price
        db.session.commit()

  