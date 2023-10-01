from mongoengine import Document, ReferenceField, FloatField

from app.models.expense import Expense
from app.models.user import User


class Transaction(Document):
    from_user = ReferenceField(User, required=True)
    to_user = ReferenceField(User, required=True)
    amount = FloatField(min_value=0, required=True)
    related_expense = ReferenceField(Expense, required=True)