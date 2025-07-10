from flask import Flask, render_template
from models import db, User
from auth import auth_bp
from api import api_bp
from flask_migrate import Migrate
from flask_login import LoginManager
from dotenv import load_dotenv
from flask.cli import with_appcontext
import click
import os

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")  # ✅ ADD THIS LINE

print(f"DEBUG: TMDB_API_KEY loaded: {'SET' if TMDB_API_KEY else 'NOT SET'}")

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movie_recommendation.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(api_bp, url_prefix='/api')

from flask_login import login_required

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/login')
def login_page():  # ✅ Correctly aligned with the decorator
    return render_template("login.html")

@app.route('/register')
def register():
    return render_template("registration.html")


@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.cli.command("create-db")
@with_appcontext
def create_db():
    db.create_all()
    click.echo("✅ Database tables created successfully!")

if __name__ == '__main__':
    if not TMDB_API_KEY:
        print("⚠️ TMDB_API_KEY not found in .env! Please set it before using TMDB features.")

    @app.route('/debug/tmdb_key')
    def debug_tmdb_key():
        if TMDB_API_KEY:
            return "TMDB_API_KEY is set"
        else:
            return "TMDB_API_KEY is NOT set"

    app.run(debug=True)
