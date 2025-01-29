"""API Program for handling requests for website pages"""

import sqlite3
from flask import (
    Flask, abort,
    render_template,
    request, redirect,
    url_for
)

from helpers.system import System
from helpers.planet import Planet
from helpers.star import Star

# flask --app main run --debug

app = Flask(__name__)

DB = "database.db"
TABLES = ['planets', 'systems', 'stars']


@app.after_request
def add_security_headers(response):
    """Add security headers to all responses"""

    # prevent inline scripts from being executed - requires checking to get google font to apply 
    # response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'none'; style-src 'self' https://fonts.googleapis.com; img-src 'self' data:;"
    
    # prevent MIME type sniffing - predicting what type a file is
    response.headers['X-Content-Type-Options'] = 'nosniff'
    # prevent clickjacking, control browser X-framing, pages cannot be embedded
    response.headers['X-Frame-Options'] = 'DENY'
    # enable browsers inbuilt XXS protection
    response.headers['X-XSS-Protection'] = '1; mode=block'
    # enable stricter CSP protection
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    # Controls the amount of referrer information with requests 
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin' #'no-referrer'

    # # Enforces HTTPS connection - requires HTTPS served site 
    # response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'

    return response

@app.route("/")
def home():
    """Renders HTML home page with current exoplanet and
    planetary systems count
    """
    exo_systems = get_exo_system_count()
    planets = get_planet_count()

    return render_template("home.html", exo_systems=exo_systems, planets=planets)


@app.route("/statistics")
def statistics():
    """Renders static page with plot images and descriptions"""
    return render_template("statistics.html")


@app.route("/new/<category>")
def new(category):
    """Generate most recent planet discoveries from planets
    database table from MAX disc_pubdate
    """
    month_going_back = 1

    if category not in ['p', 's', 'ps']:
        abort(404)

    if category in ['s', 'ps']:
        new_systems = get_systems_from_max_updated(month_going_back)


    if category in ['p', 'ps']:
        new_planets = get_planets_from_month_disc(month_going_back)


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


@app.route("/randomiser")
def randomiser():
    """Redirects to system route with random planet as stellar body"""
    random_planet = get_random_planet_name()

    return redirect(url_for('system', stellar_body=random_planet), code=302)


# @app.route("/system", strict_slashes=False)
@app.route("/system")
@app.route("/system/")
@app.route("/system/<stellar_body>")
def system(stellar_body=None):
    """Dynamically generate system page from planet, star or system name
    """

    # if navigated through html form search bar
    if 'search' in request.args:
        stellar_body = request.args.get('search')

    # if no search input in either entry case
    if not stellar_body:
        # render empty suggestions  
        return render_template("suggestions.html", suggestions=None, search=None), 302
    
    # Try to create system instance
    try:
        system = System(stellar_body)
    except TypeError:
        # if no reference to system by redirect
        return redirect(url_for('suggestions', search=stellar_body), code=302)

    size = system.num_planets + len(system.stars)

    return render_template("system.html", system=system, size=size)


@app.route("/planet/")
@app.route("/planet/<planet_name>")
def planet(planet_name=None):
    if not planet_name:
        # render empty suggestions  
        return render_template("suggestions.html", suggestions=None, search=None), 302

    try:
        planet = Planet(planet_name)
    except TypeError:
        # if no reference to system by redirect
        return redirect(url_for("suggestions", search=planet_name))
    
    return render_template("planet.html", planet=planet)


@app.route("/planet/")
@app.route("/star/<star_name>")
def star(star_name):
    if not star_name:
        # render empty suggestions  
        return render_template("suggestions.html", suggestions=None, search=None), 302

    try:
        star = Star(star_name)
    except TypeError:
        # if no reference to system by redirect
        return redirect(url_for("suggestions", search=star_name))
    
    return render_template("star.html", star=star)


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
    return render_template("suggestions.html", suggestions=suggestions, search=search)


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/declassed")
def declassified():

    planet_names = []

    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT pl_name FROM planets
            WHERE declassified = 1;
        """)
        planets = cursor.fetchall()
        planet_names.extend(planet[0] for planet in planets)
    
    declassed = []

    for planet_name in planet_names:
        declassed.extend(Planet(planet_name))

    return render_template("declassified.html", planet=declassed)

@app.errorhandler(404)
def page_not_found(error=404):
    return render_template('404.html', error=error), 404

# @app.errorhandler(Exception)
# def handle_exception(error):
#     return render_template('500.html', error=error), 500




# home helper functions
# ******************
def get_exo_system_count():
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        query = f"""
            SELECT COUNT(sy_name)
                FROM {TABLES[1]};
        """
        cursor.execute(query)

        return cursor.fetchone()[0]

def get_planet_count():
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        query = f"""
            SELECT COUNT(pl_name)
              FROM {TABLES[0]}
        """
        cursor.execute(query)
        return cursor.fetchone()[0]
# ******************

# new helper functions
# ******************
def get_systems_from_max_updated(month_var: int) -> list:
    """Returns a list of system objects that where the last updated"""
    new_planets = get_planet_names_from_month_disc(month_var)
    updated_systems = []

    for planet in new_planets:
        updated_systems.append(System(planet[0]))

    return set(updated_systems)

def get_planets_from_month_disc(month_var: int) -> list:
    """Returns a list of planet instances from the most recent discoveries
    going back x months (month_var)

    :param month_var: int """
    new_planets = []

    planets = get_planet_names_from_month_disc(month_var)

    for planet in planets:
        new_planets.append(Planet(planet[0]))

    return new_planets

def get_planet_names_from_month_disc(month_var: int) -> list:
    """Returns a list of tuples from sql query of planets
    discovered going back x months (month_var)

    planet name will be [0] of each
"""
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        query = f"""
            SELECT pl_name
            FROM {TABLES[0]}
            WHERE disc_pubdate BETWEEN
                STRFTIME('%Y-%m', DATE('now', '-{month_var} months'))
                AND
                STRFTIME('%Y-%m', DATE('now'))
            ORDER BY disc_pubdate DESC;
        """
        return cursor.execute(query)
# ******************

# randomiser helper functions
# ******************
def get_random_planet_name():
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()

        cursor.execute(f"""
            SELECT pl_name
                FROM {TABLES[0]}
                ORDER BY RANDOM()
                LIMIT 1;
        """)
        return cursor.fetchone()[0]
# ******************

# .... helper functions
# ******************
# ******************
