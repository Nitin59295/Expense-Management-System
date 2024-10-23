from flask import Blueprint, request, render_template, redirect, url_for, flash
from models import db, Expense, Revenue

main = Blueprint('main', __name__)


@main.route('/')
def home():
    return render_template('index.html')


@main.route('/expenses')
def expenses():
    return render_template('expenses.html')


@main.route('/list_expense')
def list_expense():
    expense_list = Expense.query.all()
    return render_template('list_expenses.html', expenses=expense_list)


@main.route('/list_revenue')
def list_revenue():
    revenues = Revenue.query.all()
    return render_template('list_revenue.html', revenues=revenues)


@main.route('/log_expense', methods=['GET', 'POST'])
def log_expense():
    if request.method == 'POST':
        expense_type = request.form.get('expense_type')
        quantity = request.form.get('quantity')
        item_name = request.form.get('item_name')
        unit_price = request.form.get('unit_price')
        invoice_number = request.form.get('invoice_number')
        seller_gstn = request.form.get('seller_gstn')
        gst_amount = request.form.get('gst_amount')
        user_id = int(request.form.get('user_id'))
        designation = request.form.get('designation')
        update_flag = request.form.get('update_flag') == 'on'  # Checkbox handling
        total_amount = request.form.get('total_amount')

        new_expense = Expense(
            expense_type=expense_type,
            quantity=quantity,
            item_name=item_name,
            unit_price=unit_price,
            invoice_number=invoice_number,
            seller_gstn=seller_gstn,
            gst_amount=gst_amount,
            user_id=user_id,
            designation=designation,
            update_flag=update_flag,
            total_amount=total_amount
        )

        db.session.add(new_expense)
        db.session.commit()
        flash('Expense logged successfully!', 'success')
        return redirect(url_for('main.list_expense'))
    return render_template('log_expense.html')


@main.route('/log_revenue', methods=['GET', 'POST'])
def log_revenue():
    if request.method == 'POST':
        project_name = request.form.get('project_name')
        total_estimate = request.form.get('total_estimate')
        user_id = int(request.form.get('user_id'))

        new_revenue = Revenue(
            project_name=project_name,
            total_estimate=total_estimate,
            user_id=user_id
        )

        db.session.add(new_revenue)
        db.session.commit()
        flash('Revenue logged successfully!', 'success')
        return redirect(url_for('main.list_revenue'))
    return render_template('log_revenue.html')


@main.route('/update_expense/<int:id>', methods=['GET', 'POST'])
def update_expense():
    expense = Expense.query.get(id)
    if request.method == 'POST':
        expense.expense_type = request.form.get('expense_type')
        expense.quantity = request.form.get('quantity')
        expense.item_name = request.form.get('item_name')
        expense.unit_price = request.form.get('unit_price')
        expense.invoice_number = request.form.get('invoice_number')
        expense.seller_gstn = request.form.get('seller_gstn')
        expense.gst_amount = request.form.get('gst_amount')
        expense.user_id = int(request.form.get('user_id'))
        expense.designation = request.form.get('designation')
        expense.update_flag = request.form.get('update_flag') == 'on'
        expense.total_amount = request.form.get('total_amount')

        db.session.commit()
        flash('Expense updated successfully!', 'success')
        return redirect(url_for('main.list_expense'))
    return render_template('update_expense.html', expense=expense)


@main.route('/update_revenue/<int:id>', methods=['GET', 'POST'])
def update_revenue():
    revenue = Revenue.query.get(id)
    if revenue is None:
        return "Revenue entry not found", 404
    if request.method == 'POST':
        revenue.project_name = request.form.get('project_name')
        revenue.total_estimate = request.form.get('total_estimate')
        revenue.user_id = int(request.form.get('user_id'))

        db.session.commit()
        flash('Revenue updated successfully!', 'success')
        return redirect(url_for('main.list_revenue'))
    return render_template('update_revenue.html', revenue=revenue)
