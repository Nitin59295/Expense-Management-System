from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, FloatField, IntegerField
from wtforms.validators import DataRequired

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
    submit = SubmitField('Log Expense')

class RevenueForm(FlaskForm):
    project_name = StringField('Project Name', validators=[DataRequired()])
    total_estimated_revenue = FloatField('Total Estimated Revenue', validators=[DataRequired()])
    employee_id = SelectField('Employee', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Log Revenue')
