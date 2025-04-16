from datetime import datetime
from flask_login import UserMixin
from market import db, login_manager, bcrypt

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    
    # Relationships
    items = db.relationship('Item', backref='owned_by', lazy=True, foreign_keys='Item.owner')
    cart_items = db.relationship('CartItem', backref='user', lazy=True, cascade="all, delete-orphan")
    orders = db.relationship('Order', backref='customer', lazy=True)
    
    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f'${str(self.budget)[:-3]},{str(self.budget)[-3:]}$'
        else:
            return f"${self.budget}$"
            
    @property
    def password(self):
        return self.password_hash
        
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
        
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
        
    def can_purchase(self, item_obj):
        return self.budget >= item_obj.price
        
    def can_sell(self, item_obj):
        return item_obj in self.items
        
    @property
    def cart_total(self):
        return sum(item.subtotal for item in self.cart_items)

    @property
    def cart_count(self):
        return sum(item.quantity for item in self.cart_items)

class Category(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    description = db.Column(db.String(length=256), nullable=True)
    items = db.relationship('Item', backref='category', lazy=True)
    
    def __repr__(self):
        return f'Category {self.name}'

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    image_url = db.Column(db.String(length=256), nullable=True)
    category_id = db.Column(db.Integer(), db.ForeignKey('category.id'))
    stock = db.Column(db.Integer(), default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
    
    __table_args__ = (
        db.Index('idx_item_name', 'name'),
        db.Index('idx_item_category', 'category_id'),
        db.Index('idx_item_owner', 'owner'),
    )
    
    def __repr__(self):
        return f'Item {self.name}'
        
    def buy(self, user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()
        
    def sell(self, user):
        self.owner = None
        user.budget += self.price
        db.session.commit()

class CartItem(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    item_id = db.Column(db.Integer(), db.ForeignKey('item.id'), nullable=False)
    quantity = db.Column(db.Integer(), default=1)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    item = db.relationship('Item')
    
    @property
    def subtotal(self):
        return self.item.price * self.quantity

class Order(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(length=20), default='pending')
    total_amount = db.Column(db.Integer(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    payment_id = db.Column(db.String(length=100), nullable=True)
    
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade="all, delete-orphan")
    user = db.relationship('User')

class OrderItem(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    order_id = db.Column(db.Integer(), db.ForeignKey('order.id'), nullable=False)
    item_id = db.Column(db.Integer(), db.ForeignKey('item.id'), nullable=False)
    quantity = db.Column(db.Integer(), default=1)
    price = db.Column(db.Integer(), nullable=False)  # Store price at time of purchase
    
    item = db.relationship('Item')
