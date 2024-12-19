"""API Program for handling requests for website pages"""

import sqlite3
from flask import Flask, render_template

# flask --app main run --debug

app = Flask(__name__)

DB = "database.db"
TABLES = ['planetary_systems', 'stellar_hosts', 'stellar']

@app.route("/")
def home():
    """Renders HTML home page with current exoplanet and
    exoplanetary systems count
    """
    exo_systems = 0
    planets = 0
    with sqlite3.connect(DB) as conn:
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
    """Renders static page with plot images and descriptions"""
    return render_template("discoveries.html")

@app.route("/new")
def new():
    """Generate most recent planet discoveries from planetary_systems
    database table from MAX disc_pubdate
    """
    new_systems = []
    with sqlite3.connect(DB) as conn:
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
    with sqlite3.connect(DB) as conn:
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

@app.route("/system/<stellar_body>")
def system(stellar_body):
    """Dynamically generate system page from planet or star name
    prefix query with 'p-' or 's-' to get system name from relevent database
    """
    body, body_name = stellar_body.split('-', 1)

    data = {
        'system_name': '',
        'planets': [],
        'stars': [],
        'size': 0
    }

    if body not in ['p', 'st', 'sy']:
        # fail
        pass

    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()

        if body == 'p':
            cursor.execute(f"""SELECT hostname FROM {TABLES[0]} WHERE pl_name='{body_name}'""")
            body_name = cursor.fetchone()[0]
        
        if body in ['p', 'st']:
            cursor.execute(f"""SELECT sy_name FROM {TABLES[2]} WHERE hostname='{body_name}'""")
            data['system_name'] = cursor.fetchone()[0]
        
        if body == 'sy':
            data['system_name'] = body_name


        cursor.execute(f"""
            SELECT hostname
            FROM {TABLES[2]}
            WHERE sy_name='{data['system_name']}'
        """)
        stars = cursor.fetchall()
        data['stars'] = [i[0] for i in stars]

        query = f"""
            SELECT pl_name, disc_pubdate
            FROM {TABLES[0]}
            WHERE hostname IN ({','.join('?' * len(data['stars']))})
        """
        cursor.execute(query, data['stars'])
        planets = cursor.fetchall()
        data['planets'] = list(planets)


        data['size'] = len(data['planets']) + len(data['stars']) + 1

    return render_template("system.html", data=data)





@app.route("/about")
def about():
    return render_template("about.html")
