from flask import Flask, render_template
from flask_login import LoginManager
from backend.models import db, User
from backend.auth import auth_bp
from backend.bookings import bookings_bp
from backend.events import events_bp
import os

def create_app():
    app = Flask(__name__)

    # App configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bvrit_sports.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize DB
    db.init_app(app)

    # Flask Login Manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Create DB Tables
    with app.app_context():
        db.create_all()

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(bookings_bp, url_prefix='/bookings')
    app.register_blueprint(events_bp, url_prefix='/events')

    # Base Routes
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/contact')
    def contact():
        return render_template('contact.html')

    @app.route('/faq')
    def faq():
        return render_template('faq.html')

    return app

# Run the app
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
