from manager import db


class Subscribers(db.Model):
    __tablename__ = 'subscribers'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    first_name = db.Column(db.String(64), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return "{}".format(self.email)

    def unsubscribe(self):
        self.is_active = False

    def subscribe(self):
        self.is_active = True
