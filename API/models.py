from API import db
from datetime import datetime


class Activity(db.Model):
    """
        Activities
    """

    __tablename__ = "activity"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)
    expenses = db.relationship("Expenses", backref="account", lazy="dynamic", cascade='all, delete-orphan')

    def __repr__(self):
        return f"Activity({self.title})"


class Expenses(db.Model):
    """
        Expenses
    """
    __tablename__ = "expense"

    id = db.Column(db.Integer, primary_key=True)
    expense_title = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    activity = db.Column(db.Integer, db.ForeignKey("activity.id"))

    def __repr__(self):
        return f"Activity({self.expense_title})"


class Users(db.Model):
    """
        Users
    """

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return f"Activity({self.username})"

