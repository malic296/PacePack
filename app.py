from flask import Flask
from routes.main import main
from routes.login import login
from dotenv import load_dotenv
import os

# Načtení proměnných z .env souboru
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")  # Tajný klíč pro session

# Registrace Blueprintů
app.register_blueprint(main)
app.register_blueprint(login)

if __name__ == '__main__':
    app.run(debug=True)
