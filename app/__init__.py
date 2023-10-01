from flask import Flask
from mongoengine import connect


def create_app():
    app = Flask(__name__)

    # Configure the database
    app.config["MONGO_DBNAME"] = "Splitwise"

    # Connecting to the database
    connect(db=app.config["MONGO_DBNAME"], host="mongodb://127.0.0.1:27017")

    # Register blueprints
    from app.routes import user_routes, expense_routes, transaction_routes
    app.register_blueprint(user_routes.user_bp)
    app.register_blueprint(expense_routes.expense_bp)
    app.register_blueprint(transaction_routes.transaction_bp)

    return app
