from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(15))


class Expense(db.Model):
    __tablename__ = 'expenses'

    id = db.Column(db.Integer, primary_key=True)
    expense_type = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    item_name = db.Column(db.String(100), nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    invoice_number = db.Column(db.String(50), nullable=False)
    seller_gstn = db.Column(db.String(15))
    gst_amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    logging_date = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    designation = db.Column(db.String(50), nullable=False)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    update_flag = db.Column(db.Boolean, default=False)

class Revenue(db.Model):
    __tablename__ = 'revenues'
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(50), nullable=False)
    total_estimate = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    logging_date = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    designation = db.Column(db.String(50), nullable=False)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    update_flag = db.Column(db.Boolean, default=False)

class Seller(db.Model):
    __tablename__ = 'seller'
    gstn = db.Column(db.String(15), primary_key=True)
    seller_name = db.Column(db.String(100), unique=True)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    designation = db.Column(db.String(50))
