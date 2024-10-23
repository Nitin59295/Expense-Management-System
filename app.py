from flask import Flask
from models import db
from flask_migrate import Migrate
from routes import main 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:qwerty@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(main)

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(debug=True)

