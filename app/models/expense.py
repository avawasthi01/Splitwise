from enum import Enum

from mongoengine import Document, StringField, FloatField, EnumField, ListField, DictField, ImageField, ReferenceField

from app.models.user import User


class ExpenseType(Enum):
    EQUAL = "EQUAL"
    EXACT = "EXACT"
    PERCENT = "PERCENT"


class Expense(Document):
    payer = ReferenceField(User, required=True)
    total_amount = FloatField(min_value=0, required=True)
    expense_type = EnumField(ExpenseType, required=True)
    involved_users = ListField(ReferenceField(User), required=True)
    splits = DictField()
    # For EQUAL, this could be empty.
    # For EXACT, it's a dictionary of user_id: exact_amount.
    # For PERCENT, it's a dictionary of user_id: percent_value.
