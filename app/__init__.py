import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_caching import Cache
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from market.config import config

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login_page'
login_manager.login_message_category = 'info'
csrf = CSRFProtect()
cache = Cache()
talisman = Talisman()
limiter = Limiter(key_func=get_remote_address)

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # Configure cache
    cache_config = {
        'CACHE_TYPE': 'simple',  # Use redis in production
        'CACHE_DEFAULT_TIMEOUT': 300
    }
    app.config.from_mapping(cache_config)
    cache.init_app(app)
    
    # Configure security
    csp = {
        'default-src': "'self'",
        'script-src': "'self' 'unsafe-inline' https://js.stripe.com",
        'style-src': "'self' 'unsafe-inline' https://fonts.googleapis.com",
        'img-src': "'self' data:",
        'font-src': "'self' https://fonts.gstatic.com",
        'connect-src': "'self' https://api.stripe.com"
    }
    talisman.init_app(app, content_security_policy=csp, force_https=False)  # Set to True in production
    
    limiter.init_app(app)
    
    # Set up error logging
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        from logging.handlers import RotatingFileHandler
        import logging
        file_handler = RotatingFileHandler('logs/marketplace.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('Marketplace startup')
    
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
