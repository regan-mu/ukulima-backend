from flask import jsonify, request
from API.models import Expenses, Activity
from API import app, db


@app.route("/API/expenses/create", methods=["POST"])
def create_expense():
    """
        Create expenses
        :return: 201
    """
    data = request.get_json()
    activity = Activity.query.filter_by(id=int(data["expenses"][0]["activity"])).first()
    if activity.completed:
        return jsonify(dict(message="Cannot add expenses to this activity")), 403
    for var in data["expenses"]:
        expense = Expenses(
            expense_title=var["title"],
            amount=var["amount"],
            activity=var["activity"]
        )
        db.session.add(expense)
        db.session.commit()
    return jsonify(dict(message="Expenses added successfully")), 201


@app.route("/API/expenses/delete/<expense_id>", methods=["DELETE"])
def delete_expense(expense_id):
    expense = Expenses.query.filter_by(id=expense_id).first()
    activity = Activity.query.filter_by(id=expense.activity).first()
    if activity.completed:
        return jsonify(dict(message="Cannot delete expense")), 403
    else:
        if expense:
            db.session.delete(expense)
            db.session.commit()
            return jsonify(dict(message="Delete successful")), 200
        else:
            return jsonify(dict(message="Expense not found")), 404


@app.route("/API/expense/<expense_id>", methods=["GET"])
def get_single_expense(expense_id):
    expense = Expenses.query.filter_by(id=expense_id).first()
    if expense:
        return jsonify(dict(title=expense.expense_title, amount=expense.amount)), 200
    else:
        return jsonify(dict(message="Expense not found")), 404
