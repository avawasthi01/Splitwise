from flask import request, jsonify, Blueprint
from app.models.expense import Expense

expense_bp = Blueprint('expenses', __name__)


def split_amount(amount, num_people):
    base_share = amount / num_people
    rounded_base = round(base_share, 2)
    remainder = amount - (rounded_base * num_people)

    shares = [rounded_base for _ in range(num_people)]
    for i in range(int(remainder * 100)):
        shares[i] += 0.01

    return shares


@expense_bp.route('/add_expense', methods=['POST'])
def add_expense():
    data = request.json
    expense_type = data["expense_type"]
    total_amount = data["total_amount"]

    if expense_type == "EQUAL":
        num_people = len(data["participants"])  # Assuming participants is a list of user IDs sharing the expense.
        shares = split_amount(total_amount, num_people)
        data["splits"] = dict(zip(data["participants"], shares))

    elif expense_type == "PERCENT":
        if sum(data["splits"].values()) != 100:
            return jsonify({"error": "Percent splits do not total 100%."}), 400
    elif expense_type == "EXACT":
        if sum(data["splits"].values()) != total_amount:
            return jsonify({"error": "Exact splits do not match total amount."}), 400

    expense = Expense(**data)
    expense.save()

    return jsonify({"message": "Expense added successfully"}), 201


@expense_bp.route('/expenses/<user_id>', methods=['GET'])
def show_user_expenses(user_id):
    expenses = Expense.objects(payer=user_id)
    return jsonify(expenses)
