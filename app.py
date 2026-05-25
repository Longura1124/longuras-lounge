from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# config (example)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# IMPORTANT: import routes AFTER app + db
from routes import *

# ADD THIS AT THE BOTTOM:
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # This builds your Game and User tables in Render automatically
    app.run(debug=True)