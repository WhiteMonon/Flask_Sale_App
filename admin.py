from sale_app import app, db
from flask_admin.contrib.sqla import ModelView
from models import User, Product , Category, Order
from wtforms import SelectField
from flask_admin import Admin, AdminIndexView
from flask_admin import expose
from routes import role_required
from flask import url_for
from flask_admin.menu import MenuLink
from flask_login import current_user
from flask import redirect , flash
from sqlalchemy import func
from ultils import format_currency

class UserView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == 'ADMIN'

    def inaccessible_callback(self, name, **kwargs):
        flash('Bạn không có quyền truy cập trang quản trị.', 'warning')
        return redirect(url_for('login'))
    column_display_pk = False
    column_exclude_list = ['password']  
    column_searchable_list = ['username']
    column_labels = {
        'joined_date': 'Ngày đăng ký',
        'user_role': 'Vai trò'
    }

    form_overrides = {
        'user_role': SelectField
    }
    form_args = {
        'user_role': {
            'choices': [('USER', 'Người dùng'), ('ADMIN', 'Quản trị viên')]
        }
    }

class ProductView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == 'ADMIN'

    def inaccessible_callback(self, name, **kwargs):
        flash('Bạn không có quyền truy cập trang quản trị.', 'warning')
        return redirect(url_for('login'))
    column_display_pk = False
    column_labels = {
        'name': 'Tên sản phẩm',
        'price': 'Giá',
        'category_id': 'Mã danh mục',
        'description': 'Mô tả',
        'image': 'Hình ảnh',
        'stock': 'Số lượng',
        'created_date': 'Ngày tạo'
    }

    column_list = [ 'category_id' ,'name', 'price', 'description', 'stock', 'created_date']

    column_sortable_list = ['name', 'price', 'stock']

    column_searchable_list = ['name', 'description']

    column_filters = ['price']

    form_overrides = {
        'category_id': SelectField
    }

    form_columns = ['name', 'price', 'category_id', 'description', 'image', 'stock']

    column_formatters = {
        'price': lambda view, context, model, name: f"{model.price:,.0f}"
    }

    def get_category_choices(self):
        with app.app_context():
            categories = Category.query.all()
            data = [(c.id, c.name) for c in categories]
            return data

    def create_form(self):
        form = super(ProductView, self).create_form()
        form.category_id.choices = self.get_category_choices()
        return form
    
    def edit_form(self):
        form = super(ProductView, self).edit_form()
        form.category_id.choices = self.get_category_choices()
        return form
    
class OrderView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == 'ADMIN'

    def inaccessible_callback(self, name, **kwargs):
        flash('Bạn không có quyền truy cập trang quản trị.', 'warning')
        return redirect(url_for('login'))
    
    column_display_pk = False
    column_list = ['user_id', 'total_amount', 'address', 'phone', 'payment_method', 'order_date', 'status_id']
    column_sortable_list = ['total_amount', 'order_date']
    column_searchable_list = ['user_id', 'address', 'phone', 'payment_method', 'status_id']
    column_filters = ['status_id']
    column_formatters = {
        'total_amount': lambda view, context, model, name: f"{model.total_amount:,.0f}"
    }

    can_create = False
    
    def create_form(self):
        return None
    
    form_columns = ['user_id', 'total_amount', 'address', 'phone', 'payment_method', 'order_date', 'status_id']
    
    form_overrides = {
        'status_id': SelectField
    }
    
    form_args = {
        'status_id': {
            'choices': [(1, 'Đang xử lý'), (2, 'Đã hoàn thành')]
        }
    }
    
    
    


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    @role_required('ADMIN')
    def index(self):
        total_orders = Order.query.count()
        total_revenue = db.session.query(func.sum(Order.total_amount)).filter(Order.status_id == 2).scalar() or 0
        total_products = Product.query.count()
        recent_orders = Order.query.order_by(Order.order_date.desc()).limit(5).all()

        return self.render('admin/index.html',
                           total_orders=total_orders,
                           total_revenue=total_revenue,
                           total_products=total_products,
                           recent_orders=recent_orders)
    
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == 'ADMIN'

    def inaccessible_callback(self, name, **kwargs):
        flash('Bạn không có quyền truy cập trang quản trị.', 'warning')
        return redirect(url_for('login'))

admin = Admin(app, name='Sale App', template_mode='bootstrap4', index_view=MyAdminIndexView())

admin.add_view(UserView(User, db.session))
admin.add_view(ProductView(Product, db.session))
admin.add_view(OrderView(Order, db.session))

admin.add_link(MenuLink(name='Đăng xuất', url='/logout'))