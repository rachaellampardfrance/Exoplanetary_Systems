"""API Program for handling requests for website pages"""

import sqlite3
from flask import Flask, render_template, request, redirect, url_for

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

@app.route("/statistics")
def statistics():
    """Renders static page with plot images and descriptions"""
    return render_template("statistics.html")

@app.route("/new/<category>")
def new(category):
    """Generate most recent planet discoveries from planetary_systems
    database table from MAX disc_pubdate
    """

    if category not in ['p', 's', 'ps']:
        return render_template("error.html", message="Page does not exist")

    if category in ['s', 'ps']:
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
            system_icos = ("☀️" * mod[1]) + ("🪐" * mod[2])
            new_systems.append(
                {
                    "sy_name": mod[0],
                    "sy_snum": mod[1],
                    "sy_pnum": mod[2],
                    "system_icos": system_icos
                }
            )

    if category in ['p', 'ps']:
        new_planets = []
        with sqlite3.connect(DB) as conn:
            cursor = conn.cursor()

            # List only most recently requested updates
            modified = cursor.execute("""
                SELECT *
                FROM planetary_systems
                WHERE last_updated = (
                    SELECT MAX(last_updated)
                    FROM planetary_systems
                )
                ORDER BY disc_pubdate DESC;
            """)

            # List only most recent disc_pubdate
            # modified = cursor.execute("""
            #     SELECT *
            #     FROM planetary_systems
            #     WHERE disc_pubdate = (
            #         SELECT MAX(disc_pubdate)
            #         FROM planetary_systems
            #     );
            # """)

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
    if category == 'p':
        return render_template(
            "new.html",
            new_planets=new_planets,
            category=category
        )
    elif category == 's':
        return render_template(
            "new.html",
            new_systems=new_systems,
            category=category
        )
    return render_template(
        "new.html",
        new_systems=new_systems,
        new_planets=new_planets,
        category=category
    )


@app.route("/system")
@app.route("/system/<stellar_body>")
def system(stellar_body=None):
    """Dynamically generate system page from planet, star or system name
    """

    if 'search' in request.args:
        stellar_body = request.args.get('search').lower()
    elif stellar_body:
        stellar_body = stellar_body.lower()
    else:
        # fail case
        return render_template("error.html", message="No search term or stellar body provided")

    data = {
        'system_name': '',
        'planets': [],
        'stars': [],
        'size': 0
    }
    
    name = ''

    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()

        # check planet table
        cursor.execute(f"""
            SELECT hostname
              FROM {TABLES[0]}
             WHERE LOWER(pl_name)='{stellar_body}';
        """)
        name = cursor.fetchone()
        if name:
            # check star table
            cursor.execute(f"""
                SELECT sy_name
                  FROM {TABLES[2]}
                 WHERE hostname='{name[0]}';
            """)
            data['system_name'] = cursor.fetchone()[0]
        # check star table
        else:
            cursor.execute(f"""
                SELECT sy_name
                  FROM {TABLES[2]}
                 WHERE LOWER(hostname)='{stellar_body}';
            """)
            name = cursor.fetchone()
            if name:
                data['system_name'] = name[0]
            #  check stellar_host table
            else:
                cursor.execute(f"""
                    SELECT sy_name
                      FROM {TABLES[1]}
                     WHERE LOWER(sy_name)='{stellar_body}';
                """)
                name = cursor.fetchone()
                if name:
                    data['system_name'] = name[0]
                else:
                    return redirect(url_for('suggestions', search=stellar_body), code=302)


        cursor.execute(f"""
            SELECT hostname
              FROM {TABLES[2]}
             WHERE sy_name='{data['system_name']}'
        """)
        stars = cursor.fetchall()
        data['stars'] = [i[0] for i in stars]

        query = f"""
            SELECT pl_name, disc_pubdate, hostname, cb_flag
              FROM {TABLES[0]}
             WHERE hostname
                    IN ({','.join('?' * len(data['stars']))});
        """
        cursor.execute(query, data['stars'])
        planets = cursor.fetchall()

        for planet in planets:
            cb_flag = ""
            if planet[3] == 1:
                cb_flag = "Yes"
            else:
                cb_flag = "No"
            
            data['planets'].append(
                {
                    "pl_name": planet[0],
                    "disc_pubdate": planet[1],
                    "hostname": planet[2],
                    "cb_flag": cb_flag,
                }
            )


        data['size'] = len(data['planets']) + len(data['stars']) + 1

    return render_template("system.html", data=data)

@app.route("/suggestions/<search>")
def suggestions(search):
    """Renders page with stellar body search suggestions"""
    suggestions = {
        'planets': [],
        'stars': [],
        'systems': []
    }

    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        
        # Fetch planet names
        cursor.execute(f"SELECT pl_name FROM {TABLES[0]} WHERE LOWER(pl_name) LIKE ?", (f"%{search}%",))
        planets = cursor.fetchall()
        suggestions["planets"].extend([planet[0] for planet in planets])
        
        # Fetch star names
        cursor.execute(f"SELECT hostname FROM {TABLES[2]} WHERE LOWER(hostname) LIKE ?", (f"%{search}%",))
        stars = cursor.fetchall()
        suggestions['stars'].extend([star[0] for star in stars])
        
        # Fetch system names
        cursor.execute(f"SELECT sy_name FROM {TABLES[1]} WHERE LOWER(sy_name) LIKE ?", (f"%{search}%",))
        systems = cursor.fetchall()
        suggestions['systems'].extend([system[0] for system in systems])
    return render_template("suggestions.html", suggestions=suggestions)

@app.route("/about")
def about():
    return render_template("about.html")
