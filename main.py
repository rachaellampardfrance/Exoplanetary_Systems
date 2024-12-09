from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/discoveries")
def discoveries():
    return render_template("discoveries.html")

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/about")
def about():
    return render_template("about.html")