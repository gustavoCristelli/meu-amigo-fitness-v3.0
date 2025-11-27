#app.py
#Aplicativo Flask criado e configurado

from flask import Flask
from flask_cors import CORS
from models import db
from routes import configure_routes

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    configure_routes(app)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
