from flask import Flask
from routes import main

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Set a secret key for session management

# Register the blueprint
app.register_blueprint(main)

if __name__ == '__main__':
    app.run(debug=True)
