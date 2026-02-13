from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
# DB URI loaded
# A Database Uniform Resource Identifier (DB URI) is a string that specifies all the
# information needed to connect to a database, including the database type, credentials, 
# location (host and port), and database name
    db.init_app(app)

    from .routes import main
    app.register_blueprint(main)

    return app

