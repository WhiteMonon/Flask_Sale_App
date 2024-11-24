import json
from sale_app import app , db
from datetime import datetime
from flask import session

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def load_category_json():
    return load_json('data/category.json')

def load_product_json():
    return load_json('data/products.json')

def load_user_json():
    return load_json('data/user.json')

def load_products():
    with app.app_context():
        from models import Product

        products = Product.query.all()
        return products
    
def load_products_by_category_id(category_id):
    with app.app_context():
        from models import Product

        products = Product.query.filter_by(category_id=category_id).all()
        return products

def load_category():
    with app.app_context():
        from models import Category

        categories = Category.query.all()
        return categories
    
def load_order_status_json():
    return load_json('data/order_status.json')

def update_product_prices():
    # Load products from JSON file
    products_data = load_product_json()

    with app.app_context():
        from models import Product

        for product_data in products_data:
            # Find the product in the database
            product = Product.query.filter_by(id=product_data['id']).first()
            if product:
                # Update the product price
                product.price = product_data['price']
                db.session.commit()
        print("Product prices updated successfully.")

def update_product_stock():
    products_data = load_product_json()

    with app.app_context():
        from models import Product

        # import pdb; pdb.set_trace()

        for product_data in products_data:
            product = Product.query.filter_by(id=product_data['id']).first()
            if product:
                product.stock = product_data['stock']
                db.session.commit()
        print("Product stock updated successfully.")

def update_user(user_id, address, phone , fullname):
    with app.app_context():
        from models import User

        user = User.query.filter_by(id=user_id).first()
        if user:
            user.address = address
            user.phone = phone
            user.fullname = fullname
            db.session.commit()
            return True
        return False

def format_currency(value):
    return "{:,.0f} VND".format(value)

def get_product_by_id(product_id):
    with app.app_context():
        from models import Product

        product = Product.query.filter_by(id=product_id).first()
        return product
    
def add_category_from_json():
    with app.app_context():
        from models import Category

        categories_data = load_category_json()
        for category_data in categories_data:
            category = Category(name = category_data['name'])
            db.session.add(category)
        db.session.commit()
        print("Category added successfully.")

def add_product_from_json():
    with app.app_context():
        from models import Product

        products_data = load_product_json()
        for product_data in products_data:
            product = Product(name=product_data['name'],
                               price=product_data['price'], 
                               category_id=product_data['category_id'], 
                               description=product_data['description'], 
                               image=product_data['image'],
                               stock=product_data['stock'],
                               created_date=datetime.strptime(product_data['created_date'], '%Y-%m-%dT%H:%M:%S'))
            db.session.add(product)
            db.session.commit()
        print("Product added successfully.")

def add_user_from_json():
    with app.app_context():
        from models import User

        users_data = load_user_json()
        for user_data in users_data:
            user = User(username=user_data['username'], 
                        password=user_data['password'], 
                        user_role=user_data['user_role'], 
                        joined_date=user_data['joined_date'],
                        fullname=user_data['fullname'])
            db.session.add(user)
            db.session.commit()
        print("User added successfully.")

def add_order_status_from_json():
    with app.app_context():
        from models import OrderStatus

        order_status_data = load_order_status_json()
        for order_status_data in order_status_data:
            order_status = OrderStatus(name=order_status_data['name'])
            db.session.add(order_status)
            db.session.commit()
        print("Order status added successfully.")

def create_order_item(order_id, product_id, quantity, price):
    from models import OrderItem, Product
    # import pdb; pdb.set_trace()
    
    product = Product.query.get(product_id)
    if not product or int(product.stock) < int(quantity):
        return False
    
    order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=quantity, price=price)
    product.stock -= int(quantity)
    db.session.add(order_item)
    return True

def create_order(user_id, phone, address, payment_method, total, list_order_item):
    # import pdb; pdb.set_trace()
    if list_order_item == []:
        return False
    with app.app_context():
        from models import Order , Product
        
        order = Order(user_id=user_id, phone=phone, address=address, payment_method=payment_method, total_amount=total , status_id=1)
        db.session.add(order)
        db.session.flush()
        
        for item in list_order_item:
            product = Product.query.get(item['product_id'])
            if not create_order_item(order.id, item['product_id'], item['quantity'], product.price):
                db.session.rollback()
                return False
        
        db.session.commit()
        return True

def get_user_by_username(username):

    with app.app_context():
        from models import User

        user = User.query.filter_by(username=username).first()
        return user

def get_user_by_id(user_id):
    with app.app_context():
        from models import User

        user = User.query.filter_by(id=user_id).first()
        return user

def create_user(username , password , fullname):
    with app.app_context():
        from models import User

        user = User(username=username,
                    password=password, 
                    user_role='user', 
                    joined_date=datetime.now(),
                    fullname=fullname,
                    user_role="USER")
        db.session.add(user)
        db.session.commit()
        print("User created successfully.")

def count_cart_item():
    cart = session.get('cart')
    total_item = 0
    if cart:
        for item in cart:
            total_item += int(item['quantity'])
    return total_item

def load_data():
    add_category_from_json()
    add_product_from_json()
    add_user_from_json()
    add_order_status_from_json()



if __name__ == '__main__':
    load_data()
