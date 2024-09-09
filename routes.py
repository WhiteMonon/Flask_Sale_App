from flask import render_template , request , redirect , url_for , session , flash , jsonify
from ultils import *
from flask_login import login_user , logout_user , login_required , current_user
from sale_app import login_manager
from functools import wraps
from math import ceil
app.jinja_env.filters['currency'] = format_currency

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'role' not in session or session['role'] != role:
                flash('Bạn không có quyền truy cập trang này', 'danger')
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    flash('Bạn cần đăng nhập để truy cập trang này.', 'warning')
    return redirect(url_for('login'))

@app.route('/example')
def example():
    return "This is an example route"
@app.route('/clear_cart')
def clear_cart():
    session.pop('cart')
    return redirect(url_for('index'))

@app.context_processor
def inject_categories():
    return dict(category=load_category() , current_user=current_user)

@app.route('/')
def index():
    # import pdb
    # pdb.set_trace()
    category_id = request.args.get('category_id')
    page = request.args.get('page', 1, type=int)
    per_page = 8

    if category_id:
        products = load_products_by_category_id(category_id)
    else:
        products = load_products()

    total_products = len(products)
    total_pages = ceil(total_products / per_page)
    start = (page - 1) * per_page
    end = start + per_page
    products_paginated = products[start:end]

    return render_template('index.html' , products = products_paginated , page = page , total_pages = total_pages)

@app.route('/product/<int:id>')
def product(id):
    product = get_product_by_id(id)
    return render_template('product.html' , product = product)

@app.route('/login' , methods=['get' , 'post'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user_by_username(username)
        if user and user.password == password:
            session['role'] = user.user_role
            login_user(user)
            if user.user_role == 'ADMIN':
                return redirect(url_for('admin.index'))
            return redirect(url_for('index'))
        else:
            return render_template('login.html' , error='Tên đăng nhập hoặc mật khẩu không đúng')
    return render_template('login.html')

@app.route('/register' , methods=['get' , 'post'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        fullname = request.form['fullname']
        user = get_user_by_username(username)
        if user:
            return render_template('register.html' , error='Tên đăng nhập đã tồn tại')
        else:
            if password == confirm_password:
                create_user(username , password , fullname)
                flash('Đăng ký thành công! Vui lòng đăng nhập để tiếp tục.', 'success')
                return redirect(url_for('login'))
            else:
                return render_template('register.html' , error='Mật khẩu không khớp')
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/cart')
@login_required
@role_required('USER')
def cart():
    cart = session.get('cart')
    if cart is None:
        cart = []
    products_in_cart = []
    if cart:
        for item in cart:
            item['id'] = int(item['id'])
            item['price'] = int(item['price'])
            item['quantity'] = int(item['quantity'])
            product = get_product_by_id(item['id'])
            products_in_cart.append(product)
    # import pdb
    # pdb.set_trace()
    return render_template('cart.html' , cart = cart , products_in_cart = products_in_cart)

@app.route('/count_cart_item')
def count_item_in_cart():
    return jsonify({'count': count_cart_item()})

@app.route('/api/add_to_cart' , methods=['POST'])
def add_to_cart():
    data = request.json
    id = data.get('id')
    count_product = get_product_by_id(id).stock
    if count_product == 0:
        return jsonify({
            'success': False,
            'message': 'Hết hàng'
        })
    quantity = data.get('quantity')
    price = data.get('price')
    name = data.get('name')
    cart = session.get('cart')

    if cart:
        for item in cart:
            if item['id'] == id:
                if int(item['quantity']) + int(quantity) > count_product:
                    return jsonify({
                        'success': False,
                        'message': f"Số lượng sản phẩm không đủ , bạn đã có {item['quantity']} sản phẩm trong giỏ hàng"
                    })
                item['quantity'] = int(item['quantity']) + int(quantity)
                break
        else:
            if int(quantity) > count_product:
                return jsonify({
                    'success': False,
                    'message': f"Số lượng sản phẩm không đủ , bạn đã có {item['quantity']} sản phẩm trong giỏ hàng" 
                })
            cart.append({
                'id': id,
                'quantity': quantity,
                'price': price,
                'name': name
            })
    else:
        if int(quantity) > count_product:
            return jsonify({
                'success': False,
                'message': f"Số lượng sản phẩm không đủ , số lượng thêm không thể vượt quá số lượng hàng"
            })
        cart = [{
            'id': id,
            'quantity': quantity,
            'price': price,
            'name': name
        }]
    session['cart'] = cart
    return jsonify({
        'count': count_cart_item(),
        'success': True,
        'message': 'Sản phẩm đã được thêm vào giỏ hàng!'
    })


@app.route('/api/remove_from_cart', methods=['POST'])
def remove_from_cart():
    data = request.json
    id = data.get('id')
    cart = session.get('cart', [])
    
    cart = [item for item in cart if item['id'] != id]
    
    session['cart'] = cart
    return jsonify({
        'count': count_cart_item(),
        'success': True
    })

@app.route('/api/update_cart_item', methods=['POST'])
def update_cart_item():
    data = request.json
    id = data.get('id')
    quantity = data.get('quantity')
    print(quantity)
    cart = session.get('cart', [])
    count_product = get_product_by_id(id).stock
    for item in cart:
        if item['id'] == id:
            if int(quantity) > int(count_product):
                return jsonify({'success': False ,
                                'message': f"Số lượng sản phẩm không đủ , bạn đã có {count_product} sản phẩm trong giỏ hàng"
                                })
            item['quantity'] = quantity
            break
    
    session['cart'] = cart
    return jsonify({'success': True , 'count': count_cart_item()})

@app.route('/api/get_cart_total_item', methods=['POST'])
def get_cart_total_item():
    data = request.json
    id = data.get('id')
    cart = session.get('cart')
    total = sum(int(item['price']) * int(item['quantity']) for item in cart if item['id'] == id)
    formatted_total = format_currency(total)
    return jsonify({'total': formatted_total})


@app.route('/api/get_cart_total')
def get_cart_total():
    cart = session.get('cart')
    if cart:
        total = sum(int(item['price']) * int(item['quantity']) for item in cart)
        formatted_total = format_currency(total)
    else:
        formatted_total = format_currency(0)
    return jsonify({'total': formatted_total})

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/api/update_profile', methods=['POST'])
def update_profile():
    data = request.json
    address = data.get('address')
    phone = data.get('phone')
    fullname = data.get('fullname')
    if update_user(current_user.id, address, phone , fullname):
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

@app.route('/checkout')
@login_required
def checkout():
    cart = session.get('cart')
    if cart is None:
        cart = []
    total = sum(int(item['price']) * int(item['quantity']) for item in cart)
    formatted_total = format_currency(total)

    return render_template('checkout.html' , formatted_total = formatted_total)

@app.route('/api/checkout', methods=['POST'])
def Oder():
    data = request.json
    phone = data.get('phone')
    address = data.get('address')
    payment_method = data.get('paymentMethod')
    cart = session.get('cart')
    if cart is None:
        return jsonify({'success': False , 'message': 'Giỏ hàng trống'})
    total = sum(int(item['price']) * int(item['quantity']) for item in cart)
    list_order_item = []
    for item in cart:
        list_order_item.append({
            'product_id': item['id'],
            'quantity': item['quantity']
        })
    
    if create_order(current_user.id, phone, address, payment_method, total , list_order_item):
        if 'cart' in session:
            session.pop('cart')
        return jsonify({'success': True, 'message': 'Đặt hàng thành công'})
    else:
        return jsonify({'success': False , 'message': 'Đặt hàng thất bại'})

@app.route('/admin')
@role_required('ADMIN')
def admin():
    return render_template('admin/index.html')