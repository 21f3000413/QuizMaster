from flask import Flask
from backend.models import *

app = None

def setup_app():
    global app
    app = Flask(__name__)
    app.secret_key = "your_secret_key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quiz_info.sqlite3"
    db.init_app(app)
    app.app_context().push()
    print("Welcome to the website....")

    
setup_app()

from backend.controllers import *

if __name__ == "__main__":
    app.run(debug=True)