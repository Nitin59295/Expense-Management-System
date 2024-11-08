from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(100), nullable=False)

class Expense(db.Model):
    __tablename__ = 'expenses'
    id = db.Column(db.Integer, primary_key=True)
    expense_type = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    item_name = db.Column(db.String(100), nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    invoice_number = db.Column(db.String(100), nullable=False)
    seller_GSTN = db.Column(db.String(15), nullable=False)
    seller_name = db.Column(db.String(100), nullable=False)
    gst_amount = db.Column(db.Float, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    update_flag = db.Column(db.Boolean, default=False)  # New flag for updates

    employee = db.relationship('Employee', backref='expenses')
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)  # Link to Project

    @property
    def total_amount(self):
        """Calculate total expense including GST."""
        return (self.unit_price * self.quantity) + self.gst_amount

class Revenue(db.Model):
    __tablename__ = 'revenues'
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100), nullable=False)
    total_estimated_revenue = db.Column(db.Float, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    update_flag = db.Column(db.Boolean, default=False)  # New flag for updates
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)  # Link to Project
    employee = db.relationship('Employee', backref='revenues')

class Seller(db.Model):
    __tablename__ = 'sellers'
    id = db.Column(db.Integer, primary_key=True)
    gstn = db.Column(db.String(15), unique=True, nullable=False)  # GSTN must be unique
    name = db.Column(db.String(100), nullable=False)

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=True)

#setting the relationships
    expenses = db.relationship('Expense', backref='project', lazy=True)
    revenues = db.relationship('Revenue', backref='project', lazy=True)
