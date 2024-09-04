from sqlalchemy import Column, Integer, String, ForeignKey , Float , DateTime , Boolean
from sqlalchemy.orm import relationship
from sale_app import db
from datetime import datetime
from flask_login import UserMixin

class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True , autoincrement=True)

class Category(BaseModel):
    __tablename__ = 'category'
    name = Column(String(50), nullable=False)
    products = relationship('Product', backref='category', lazy=True)
    

class Product(BaseModel):
    __tablename__ = 'product'
    name = Column(String(50), nullable=False)
    price = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    description = Column(String(255), nullable=False)
    image = Column(String(255), nullable=False)
    stock = Column(Integer, nullable=False , default=0)
    created_date = Column(DateTime(50), nullable=False,  default=datetime.now())
    
class User(BaseModel , UserMixin):
    
    __tablename__ = 'user'
    username = Column(String(50), nullable=False, unique=True)
    fullname = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)
    joined_date = Column(DateTime, default=datetime.now())
    address = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    user_role = Column(String(20), default='USER')

class OrderStatus(BaseModel):
    __tablename__ = 'order_status'
    name = Column(String(20), nullable=False)

class Order(BaseModel):
    __tablename__ = 'order'
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    total_amount = Column(Float, nullable=False)
    address = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    payment_method = Column(String(20), nullable=False)
    order_date = Column(DateTime, default=datetime.now())
    status_id = Column(Integer, ForeignKey('order_status.id'), nullable=False)

    order_status = relationship('OrderStatus', backref='orders')
    user = relationship('User', backref='orders')
    order_items = relationship('OrderItem', backref='order', lazy=True)

class OrderItem(BaseModel):
    __tablename__ = 'order_item'
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    
    product = relationship('Product')


