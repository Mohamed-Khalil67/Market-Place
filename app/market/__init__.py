from flask import Flask, render_template
import os
from market.extensions import db, bcrypt, login_manager, csrf, cache

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # Load configuration
    from market.config import config
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    cache.init_app(app)
    
    # Register blueprints
    from market.blueprints.auth import auth_bp
    from market.blueprints.main import main_bp
    from market.blueprints.products import products_bp
    from market.blueprints.cart import cart_bp
    from market.blueprints.orders import orders_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(products_bp, url_prefix='/products')
    app.register_blueprint(cart_bp, url_prefix='/cart')
    app.register_blueprint(orders_bp, url_prefix='/orders')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    return app
