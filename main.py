from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

db = "database.db"

@app.route("/")
def home():
    exo_systems = 0
    planets = 0
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(sy_name)
            FROM stellar_hosts
        """)
        exo_systems = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(pl_name)
            FROM planetary_systems
        """)
        planets = cursor.fetchone()[0]

    return render_template("home.html", exo_systems=exo_systems, planets=planets)

@app.route("/discoveries")
def discoveries():
    return render_template("discoveries.html")

@app.route("/new")
def new():
    new_systems = []
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()

        modified = cursor.execute("""
            SELECT *
            FROM stellar_hosts
            WHERE last_updated = (
                SELECT MAX(last_updated)
                FROM stellar_hosts
            );
        """)

    for mod in modified:
        new_systems.append(
            {
                "sy_name": mod[0],
                "sy_snum": mod[1],
                "sy_pnum": mod[2],
            }
        )

    new_planets = []
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()

        modified = cursor.execute("""
            SELECT *
            FROM planetary_systems
            WHERE disc_pubdate = (
                SELECT MAX(disc_pubdate)
                FROM planetary_systems
            );
        """)

    for mod in modified:
        cb_flag = ""
        if mod[4] == 1:
            cb_flag = "Yes"
        else:
            cb_flag = "No"
        
        planet_icos = ("☀️" * mod[2]) + ("🪐" * mod[3])

        new_planets.append(
            {
                "pl_name": mod[0],
                "hostname": mod[1],
                "sy_snum": mod[2],
                "sy_pnum": mod[3],
                "cb_flag": cb_flag,
                "disc_pubdate": mod[5],
                "planet_icos": planet_icos
            }
        )
    return render_template("new.html", new_systems=new_systems, new_planets=new_planets)

@app.route("/about")
def about():
    return render_template("about.html")