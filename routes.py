from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Employee, Expense, Revenue, Seller, Project
from forms import EmployeeForm, ExpenseForm, RevenueForm, ReportForm, ExpenseRevenueForm
from datetime import datetime


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
    form.project_id.choices = [(p.id, p.name) for p in Project.query.all()]
    if form.validate_on_submit():
   
        gstn = form.seller_GSTN.data
        seller_name = form.seller_name.data
        existing_seller = Seller.query.filter_by(gstn=gstn).first()

        if existing_seller and existing_seller.name != seller_name:
            print('Error: The seller name does not match the registered GSTN number.', 'error')
            return render_template('expense_form.html', form=form)

        if not existing_seller:
            new_seller = Seller(gstn=gstn, name=seller_name)
            db.session.add(new_seller)  

        new_expense = Expense(
            expense_type=form.expense_type.data,
            quantity=form.quantity.data,
            item_name=form.item_name.data,
            unit_price=form.unit_price.data,
            invoice_number=form.invoice_number.data,
            seller_GSTN=gstn,
            seller_name=seller_name,
            gst_amount=form.gst_amount.data,
            employee_id=form.employee_id.data
        )

        db.session.add(new_expense)
        db.session.commit()
        
        return redirect(url_for('main.list_expenses'))
    
    return render_template('expense_form.html', form=form)

@main.route('/expenses')
def list_expenses():
    expenses = Expense.query.all()
    total_expense_amount = sum(expense.total_amount for expense in expenses)
    return render_template('expense_list.html', expenses=expenses, total_expense_amount=total_expense_amount)

@main.route('/revenue/new', methods=['GET', 'POST'])
def add_revenue():
    form = RevenueForm()
    form.employee_id.choices = [(e.id, f'{e.name} - {e.designation}') for e in Employee.query.all()]
    form.project_id.choices = [(p.id, p.name) for p in Project.query.all()]
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

@main.route('/expense/update/<int:expense_id>', methods=['GET', 'POST'])

def update_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    form = ExpenseForm(obj=expense)
    form.employee_id.choices = [(e.id, f'{e.name} - {e.designation}') for e in Employee.query.all()]

    if form.validate_on_submit():
        expense.expense_type = form.expense_type.data
        expense.quantity = form.quantity.data
        expense.item_name = form.item_name.data
        expense.unit_price = form.unit_price.data
        expense.invoice_number = form.invoice_number.data
        expense.seller_GSTN = form.seller_GSTN.data
        expense.seller_name = form.seller_name.data
        expense.gst_amount = form.gst_amount.data
        expense.update_flag = True  # Set update flag to true
        
        db.session.commit()
        return redirect(url_for('main.list_expenses'))
    
    return render_template('expense_form.html', form=form)

@main.route('/projects')
def list_projects():
    projects = Project.query.all()
    return render_template('project_list.html', projects=projects)

@main.route('/project/<int:project_id>')
def project_details(project_id):
    project = Project.query.get_or_404(project_id)
    total_expense = sum(expense.total_amount for expense in project.expenses)
    total_revenue = sum(revenue.total_estimated_revenue for revenue in project.revenues)
    return render_template(
        'project_details.html',
        project=project,
        total_expense=total_expense,
        total_revenue=total_revenue
    )

@main.route('/reports', methods=['GET', 'POST'])
def generate_report():
    form = ReportForm()

    # Populate the project choices dynamically in the route, not in the form class
    projects = Project.query.all()
    form.project_id.choices = [(0, 'All Projects')] + [(p.id, p.name) for p in projects]

    if form.validate_on_submit():
        filters = []

        # Apply filters if necessary
        if form.project_id.data != 0:
            filters.append(Expense.project_id == form.project_id.data)
            filters.append(Revenue.project_id == form.project_id.data)

        if form.start_date.data:
            filters.append(Expense.date >= form.start_date.data)
            filters.append(Revenue.date >= form.start_date.data)

        if form.end_date.data:
            filters.append(Expense.date <= form.end_date.data)
            filters.append(Revenue.date <= form.end_date.data)

        # Query the expenses and revenues based on the applied filters
        expenses = Expense.query.filter(*filters).all()
        revenues = Revenue.query.filter(*filters).all()

        return render_template('report_view.html', expenses=expenses, revenues=revenues, form=form)

    return render_template('report_form.html', form=form)

@main.route('/log_expense', methods=['GET', 'POST'])
def log_expense():
    form = ExpenseRevenueForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            # Process form data and save expense
            employee_id = form.employee_name.data
            employee_designation = form.employee_designation.data
            # Save the expense and revenue details to the database here

    # When designation is selected, populate names accordingly
    if form.employee_designation.data:
        form.populate_employee_names(form.employee_designation.data)

    return render_template('log_expense.html', form=form)