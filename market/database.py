from market import db, login_manager
from market import bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), unique=True, nullable=False)
    email = db.Column(db.String(length=50), unique=True, nullable=False)
    password = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('Items', backref='owned_user', lazy=True)

    @property
    def comma_budget(self):
        return f"{self.budget:,}"

    @property
    def hash_password(self):
        return self.hash_password

    @hash_password.setter
    def hash_password(self, pass_txt):
        self.password = bcrypt.generate_password_hash(pass_txt).decode('utf-8')

    def password_check(self, attempted_password):
        return bcrypt.check_password_hash(self.password, attempted_password)

    def budget_check(self, item_obj):
        return self.budget > item_obj.price

    def owner_check(self, item_obj):
        return item_obj in self.items

    def __repr__(self):
        return "\n".join([
            f"<Username {self.username}>",
            f"<Email {self.email}>",
            f"<Budget {self.budget}>"
        ])


class Items(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    owner_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def buy(self, user):
        self.owner_id = user.id
        user.budget -= self.price
        db.session.commit()

    def sell(self, user):
        self.owner_id = None
        user.budget += self.price
        db.session.commit()

    def __repr__(self):
        return "\n".join([
            f"<Name {self.name}>",
            f"<Barcode {self.barcode}>",
            f"<Price {self.price}>",
            f"<Desc {self.description}>"
        ])
