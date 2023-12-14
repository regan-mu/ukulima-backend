from flask import jsonify, request
from API.models import Activity
from API import app, db


@app.route("/API/activity/<activity_id>", methods=["GET"])
def get_activity(activity_id):
    """
        Get and activity
        :param activity_id: Activity id
        :return: Activity or 404
    """
    activity = Activity.query.filter_by(id=activity_id).first()
    if activity:
        activity_cost = 0
        activity_expense = []
        expenses = activity.expenses.all()
        for expense in expenses:
            activity_cost += expense.amount
            activity_expense.append(
                dict(title=expense.expense_title, amount=expense.amount, expense_id=expense.id)
            )

        return jsonify(
            dict(
                title=activity.title,
                date=activity.date.strftime("%d %b %Y"),
                complete=activity.completed,
                amountSpent=activity_cost,
                expenses=activity_expense,
                activity_id=activity.id
            )
        ), 200
    else:
        return jsonify(dict(message="Activity not found")), 404


@app.route("/API/activities/create", methods=["POST"])
def create_activity():
    """
        Create a new activity
        :return: 201
    """
    data = request.get_json()
    activity = Activity(
        title=data["title"]
    )
    db.session.add(activity)
    db.session.commit()
    return jsonify(dict(message="Activity added successfully")), 201


@app.route("/API/activities/all", methods=["GET"])
def get_all_activities():
    activities = Activity.query.order_by(Activity.date.desc()).all()
    total_expenses = 0
    result = []
    for activity in activities:
        expenses = []
        activity_amount = 0
        for expense in activity.expenses.all():
            total_expenses += expense.amount
            activity_amount += expense.amount
            expenses.append({'expense_title': expense.expense_title, 'expense_amount': expense.amount})
        result.append({
            'activity_id': activity.id,
            'activity_name': activity.title,
            'expenses': expenses,
            'activityAmount': activity_amount,
            'status': activity.completed,
            'date': activity.date.strftime("%d %b %Y")
        })

    return jsonify(dict(activities=result, amountSpent=total_expenses)), 200


@app.route("/API/activities/delete/<activity_id>", methods=["DELETE"])
def delete_activity(activity_id):
    """
        Deletes an activity
        :param activity_id: ID for activity to be deleted
        :return: 204 or 404
    """
    activity = Activity.query.filter_by(id=activity_id).first()
    if activity:
        if len(activity.expenses.all()) > 0:
            return jsonify(dict(message="Activity can't be deleted")), 403
        db.session.delete(activity)
        db.session.commit()
        return jsonify(dict(message='Activity Deleted')), 200
    else:
        return jsonify(dict(message="Activity not found")), 404


@app.route("/API/activity/<activity_id>/complete", methods=["PUT"])
def close_activity(activity_id):
    activity = Activity.query.filter_by(id=activity_id).first()
    if activity:
        activity.completed = True
        db.session.commit()
        return jsonify(dict(message="Activity completed")), 200
    else:
        return jsonify(dict(message="Activity not found")), 404


@app.route("/API/activity/<activity_id>/reopen", methods=["PUT"])
def reopen_activity(activity_id):
    activity = Activity.query.filter_by(id=activity_id).first()
    if activity:
        activity.completed = False
        db.session.commit()
        return jsonify(dict(message="Activity reopened")), 200
    else:
        return jsonify(dict(message="Activity not found")), 404

