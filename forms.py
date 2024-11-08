from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, FloatField, DateField
from wtforms.validators import DataRequired
from models import db, Employee


class EmployeeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    designation = SelectField('Designation', choices=[
        ('Manager','Manager'),
        ('Developer', 'Developer'),
        ('Designer', 'Designer'),
        ('Tester', 'Tester'),
    ], validators=[DataRequired()])
    submit = SubmitField('Submit')

class ExpenseForm(FlaskForm):
    expense_type = StringField('Expense Type', validators=[DataRequired()])
    quantity = FloatField('Quantity', validators=[DataRequired()])
    item_name = StringField('Item Name', validators=[DataRequired()])
    unit_price = FloatField('Unit Price', validators=[DataRequired()])
    invoice_number = StringField('Invoice Number', validators=[DataRequired()])
    seller_GSTN = StringField('Seller GSTN', validators=[DataRequired()])
    seller_name = StringField('Seller Name', validators=[DataRequired()])
    gst_amount = FloatField('GST Amount', validators=[DataRequired()])
    employee_id = SelectField('Employee', coerce=int, validators=[DataRequired()])
    project_id = SelectField('Project', coerce=int, validators=[DataRequired()])  # New project selection
    submit = SubmitField('Log Expense')

class RevenueForm(FlaskForm):
    project_name = StringField('Project Name', validators=[DataRequired()])
    total_estimated_revenue = FloatField('Total Estimated Revenue', validators=[DataRequired()])
    employee_id = SelectField('Employee', coerce=int, validators=[DataRequired()])
    project_id = SelectField('Project', coerce=int, validators=[DataRequired()])  # New project selection
    submit = SubmitField('Log Revenue')

class ReportForm(FlaskForm):
    project_id = SelectField('Project', coerce=int, choices=[(0, 'All Projects')])  # Set initial empty choice
    start_date = DateField('Start Date', format='%Y-%m-%d')
    end_date = DateField('End Date', format='%Y-%m-%d')
    report_type = SelectField('Report Type', choices=[('expense', 'Expense'), ('revenue', 'Revenue'), ('both', 'Both')])

    submit = SubmitField('Generate Report')

class ExpenseRevenueForm(FlaskForm):
    employee_name = SelectField('Employee Name', coerce=int, validators=[DataRequired()])
    employee_designation = SelectField('Employee Designation', coerce=str, validators=[DataRequired()])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate designation dropdown dynamically
        self.employee_designation.choices = [(d, d) for d in db.session.query(Employee.designation.distinct()).all()]

    def populate_employee_names(self, designation):
        # Populate name dropdown based on designation
        employees = Employee.query.filter_by(designation=designation).all()
        self.employee_name.choices = [(e.id, e.name) for e in employees]
