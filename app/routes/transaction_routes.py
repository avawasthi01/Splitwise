from app.models.transaction import Transaction
from app.models.user import User
from flask import render_template, request, jsonify, Blueprint

transaction_bp = Blueprint('transactions', __name__)


@transaction_bp.route('/transactions', methods=['GET'])
def list_transactions():
    user_id = request.args.get('user_id')

    if user_id:
        # Fetch transactions related to a specific user
        try:
            user = User.objects.get(id=user_id)
            transactions = Transaction.objects(participants=user).to_json()
        except:
            return jsonify({"error": "User not found"}), 404
    else:
        # Fetch all transactions if no specific user is specified
        transactions = Transaction.objects().to_json()

    return jsonify(transactions)


@transaction_bp.route('/transactions/verify', methods=['GET'])
def verify_transactions():
    transactions = Transaction.objects()
    for txn in transactions:
        # For percentage type transactions
        if txn.expense_type == 'PERCENT':
            if not sum(txn.splits.values()) == 100:
                return jsonify({"error": f"Transaction {txn.id} does not sum up to 100%"}), 400

        # For exact type transactions
        if txn.expense_type == 'EXACT':
            if not sum(txn.splits.values()) == txn.amount:
                return jsonify({"error": f"Transaction {txn.id} does not sum up to the exact amount"}), 400

    return jsonify({"message": "All transactions are verified and valid"}), 200


from collections import defaultdict

@transaction_bp.route('/balances', methods=['GET'])
def show_balances():
    # Fetch all transactions
    transactions = Transaction.objects()

    # Initialize a dictionary to calculate and store balances
    balances = defaultdict(lambda: defaultdict(float))

    # Process transactions and calculate balances
    for txn in transactions:
        payer = txn.payer_id
        # This assumes that the `splits` field in Transaction contains amounts owed by each user
        for user, amount in txn.splits.items():
            if payer != user:
                balances[payer][user] += amount
                balances[user][payer] -= amount

    # Simplify the balances (i.e., if A owes B $10 and B owes A $5, it should show A owes B $5)
    for user1 in balances:
        for user2 in balances[user1]:
            if balances[user1][user2] < 0:
                if user2 in balances and user1 in balances[user2]:
                    balances[user2][user1] = -balances[user1][user2]
                    del balances[user1][user2]


    result = {user: dict(balances[user]) for user in balances if any(value != 0 for value in balances[user].values())}

    return jsonify(result)

