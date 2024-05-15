from flask import Flask, render_template, request, jsonify
from mydb import Database
from flask import g

app = Flask(__name__, template_folder='template')
#app = Flask(__name__)
db = Database(db='myexpense.db')

# Render the index.html template
@app.route('/')
def index():
    records = db.fetchRecord('SELECT rowid, * FROM expense_record')
    total_expense_row = db.fetchRecord('SELECT SUM(item_price) FROM expense_record')[0]
    total_expense = total_expense_row[0] if total_expense_row[0] is not None else 0
    budget = db.fetchBudget()
    if budget is None:
        # Handle case where budget is not set yet
        # You can redirect to a page where the user can set the budget
        pass
    return render_template('index.html', records=records, total_expense=total_expense, budget=budget)

# Save record route
@app.route('/save_record', methods=['POST'])
def save_record():
    item_name = request.form['item_name']
    item_amt = float(request.form['item_amt'])
    transaction_date = request.form['transaction_date']

    total_expense_row = db.fetchRecord('SELECT SUM(item_price) FROM expense_record')[0]
    total_expense = total_expense_row[0] if total_expense_row[0] is not None else 0
    budget = db.fetchBudget()

    if total_expense + item_amt > budget:
        return jsonify({'status': 'error', 'message': f'The total expense will exceed the monthly budget of {budget}.'})
    else:
        db.insertRecord(item_name=item_name, item_price=item_amt, purchase_date=transaction_date)
        new_total_expense = total_expense + item_amt
        balance_remaining = budget - new_total_expense
        return jsonify({'status': 'success', 'message': 'Record saved successfully.', 'total_expense': new_total_expense, 'balance_remaining': balance_remaining})

# Update record route
@app.route('/update_record', methods=['POST'])
def update_record():
    item_name = request.form['item_name']
    item_amt = float(request.form['item_amt'])
    transaction_date = request.form['transaction_date']
    selected_rowid = request.form['selected_rowid']

    db.updateRecord(item_name=item_name, item_price=item_amt, purchase_date=transaction_date, rid=selected_rowid)
    total_expense_row = db.fetchRecord('SELECT SUM(item_price) FROM expense_record')[0]
    total_expense = total_expense_row[0] if total_expense_row[0] is not None else 0
    budget = db.fetchBudget()
    balance_remaining = budget - total_expense
    return jsonify({'status': 'success', 'message': 'Record updated successfully.', 'total_expense': total_expense, 'balance_remaining': balance_remaining})

# Delete record route
@app.route('/delete_record', methods=['POST'])
def delete_record():
    selected_rowid = request.form['selected_rowid']
    db.removeRecord(selected_rowid)
    total_expense_row = db.fetchRecord('SELECT SUM(item_price) FROM expense_record')[0]
    total_expense = total_expense_row[0] if total_expense_row[0] is not None else 0
    budget = db.fetchBudget()
    balance_remaining = budget - total_expense
    return jsonify({'status': 'success', 'message': 'Record deleted successfully.', 'total_expense': total_expense, 'balance_remaining': balance_remaining})

# Set budget route
@app.route('/set_budget', methods=['POST'])
def set_budget():
    budget = float(request.form['budget'])
    db.saveBudget(budget)  # Save or update budget in the database
    total_expense_row = db.fetchRecord('SELECT SUM(item_price) FROM expense_record')[0]
    total_expense = total_expense_row[0] if total_expense_row[0] is not None else 0
    balance_remaining = budget - total_expense
    return jsonify({'status': 'success', 'message': f'Monthly budget set to {budget}.', 'total_expense': total_expense, 'balance_remaining': balance_remaining})


if __name__ == '__main__':
    app.run(debug=True)
