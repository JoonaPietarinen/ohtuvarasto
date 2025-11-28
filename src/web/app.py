"""Flask application factory."""
from flask import Flask


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.secret_key = 'dev-secret-key-change-in-production'

    from web.routes import warehouses, products
    app.register_blueprint(warehouses.bp)
    app.register_blueprint(products.bp)

    return app
