from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, AdminIndexView, BaseView, expose
app = Flask(__name__)
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secretkey'
db = SQLAlchemy(app)
@app.get('/')
def index():
    return render_template('index.html')
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=False)
    about_company = db.Column(db.String(255), nullable=True)
class Executor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=False)
    experience = db.Column(db.String(255), nullable=True)
class AnyPageView(BaseView):
    @expose('/')
    def any_page(self):
        return self.render('admin/any_page/index.html')
class DashBoardView(AdminIndexView):
    @expose('/')
    def quer(self):
        all_customer = Customer.query.all()
        all_executor = Executor.query.all()
        return self.render('admin/dashboard_index.html', all_customer=all_customer, all_executor=all_executor)
admin = Admin(app, name='Мой сайт', template_mode='bootstrap3', index_view=DashBoardView(), endpoint='admin')
admin.add_view(ModelView(Customer, db.session, name='Заказчик'))
admin.add_view(ModelView(Executor, db.session, name='Исполнитель'))
admin.add_view(AnyPageView(name='Любая страница'))
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)