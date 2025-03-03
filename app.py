from flask import Flask
from routes.auth import auth
from routes.main import main

app = Flask(__name__)  
app.config['SECRET_KEY'] = 'd804bf8c95bb7bf98a8eeb4c367e9d54'  

app.register_blueprint(auth)  
app.register_blueprint(main)  

if __name__ == "__main__":
    app.run(debug=True)  
