from flask import render_template, redirect, url_for

def register_routes(app):
    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/prediction")
    def prediction():
        return render_template("prediction.html")
    
    @app.route("/prediction_table")
    def prediction_table():
        return render_template("prediction_table.html")

    @app.route("/volver-inicio")
    def volver_inicio():
        return redirect(url_for("home"))
