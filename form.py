from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField, SubmitField
from  wtforms.validators import DataRequired
class Expenseform(FlaskForm):
    expense_type = StringField('Expense Type', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    item_name = StringField('Item Name', validators=[DataRequired()])
    unit_price = FloatField('Unit Price', validators=[DataRequired()])
    invoice_number = IntegerField('Invoice Number', validators=[DataRequired()])
    seller_gstin = StringField('Seller GSTIN', validators=[DataRequired()])
    seller_name = StringField('Seller Name', validators=[DataRequired()])
    gst_amount = FloatField('Gst Amount', validators=[DataRequired()])
    logged_by = StringField('Loggers Name', validators=[DataRequired()])
    designation = SelectField('Designation', choices=[('Manager', 'Manager'), ('Staff', 'Staff'), ('Admin', 'Admin')], validators=[DataRequired()])
    submit = SubmitField('Log Expense')

class Revenueform(FlaskForm):
    project_name = StringField('project Name', validators=[DataRequired()])
    total_estimated_revenue = FloatField('Total Estimated Revenue', validators=[DataRequired()])
    designation = SelectField('Designation', choices=[('Manager', 'Manager'), ('Staff', 'Staff'), ('Admin', 'Admin')], validators=[DataRequired()])
    submit = SubmitField('Log Expense')

