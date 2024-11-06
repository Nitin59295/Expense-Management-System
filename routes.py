from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Employee, Expense, Revenue
from forms import EmployeeForm, ExpenseForm, RevenueForm
main = Blueprint('main', __name__)

@main.route('/')
def index():
    employees = Employee.query.all()
    return render_template('employee_list.html', employees=employees)

@main.route('/employee/new', methods=['GET', 'POST'])
def add_employee():
    form = EmployeeForm()
    if form.validate_on_submit():
        try:
            new_employee = Employee(name=form.name.data, designation=form.designation.data)
            db.session.add(new_employee)
            db.session.commit()
            return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()  # Rollback on error
            print(f"Error: {e}")  # Log the error for debugging
    return render_template('employee_form.html', form=form)

@main.route('/employees')
def list_employees():
    employees = Employee.query.all()  # Fetch all employees from the database
    return render_template('employee_list.html', employees=employees)

@main.route('/employee/edit/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    employee = Employee.query.get_or_404(id)
    form = EmployeeForm(obj=employee)
    if form.validate_on_submit():
        employee_name = form.name.data
        employee.designation = form.designation.data
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('employee_form.html', form=form, employee=employee)        

@main.route('/employee/delete/<int:id>', methods=['POST'])
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    return redirect(url_for('main.index'))

@main.route('/expense/new', methods=['GET', 'POST'])
def add_expense():
    form = ExpenseForm()
    form.employee_id.choices = [(e.id, f'{e.name} - {e.designation}') for e in Employee.query.all()]
    if form.validate_on_submit():
        new_expense = Expense(
            expense_type=form.expense_type.data,
            quantity=form.quantity.data,
            item_name=form.item_name.data,
            unit_price=form.unit_price.data,
            invoice_number=form.invoice_number.data,
            seller_GSTN=form.seller_GSTN.data,
            seller_name=form.seller_name.data,
            gst_amount=form.gst_amount.data,
            employee_id=form.employee_id.data
        )
        db.session.add(new_expense)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('expense_form.html', form=form)

@main.route('/expenses')
def list_expenses():
    expenses = Expense.query.all()
    return render_template('expense_list.html', expenses=expenses)

@main.route('/revenue/new', methods=['GET', 'POST'])
def add_revenue():
    form = RevenueForm()
    form.employee_id.choices = [(e.id, f'{e.name} - {e.designation}') for e in Employee.query.all()]
    if form.validate_on_submit():
        new_revenue = Revenue(
            project_name=form.project_name.data,
            total_estimated_revenue=form.total_estimated_revenue.data,
            employee_id=form.employee_id.data
        )
        db.session.add(new_revenue)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('revenue_form.html', form=form)

@main.route('/revenues')
def list_revenues():
    revenues = Revenue.query.all()
    return render_template('revenue_list.html', revenues=revenues)