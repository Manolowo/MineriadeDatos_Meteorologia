from flask import Flask
from web_commonwealth.routes import register_routes

app = Flask(__name__)
app.secret_key = "clave_provisoria"
register_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
