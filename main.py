"""API Program for handling requests for website pages"""

import sqlite3
from flask import (
    Flask, render_template,
    request, redirect,
    url_for
)
import re

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


@app.route("/randomiser")
def randomiser():
    """Redirects to system route with random planet as stellar body"""
    stellar_body = ""

    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()

        cursor.execute(f"""
            SELECT pl_name
              FROM {TABLES[0]}
             ORDER BY RANDOM()
             LIMIT 1;
        """)
        stellar_body = cursor.fetchone()[0]

    return redirect(url_for('system', stellar_body=stellar_body), code=302)


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
            SELECT hostname, st_spectype
              FROM {TABLES[2]}
             WHERE sy_name='{data['system_name']}'
        """)
        stars = cursor.fetchall()

        for star in stars:
            spec = ""
            spec_details = {}
            if star[1]:
                spec = star[1]
                spec_details = get_spec_type(spec)
            else:
                spec = "Unknown"

            dictionary = {
                "hostname": star[0],
                "st_spectype": spec,
            }
            # merge dictionaries
            new_dict = {**dictionary, **spec_details}
            data['stars'].append(new_dict)

        stars = [i[0] for i in stars]
        # add in fetching host star and spectral type

        query = f"""
            SELECT pl_name, disc_pubdate, hostname, cb_flag
              FROM {TABLES[0]}
             WHERE hostname
                    IN ({','.join('?' * len(stars))});
        """
        cursor.execute(query, stars)
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


#  handling star class information
# *******
def get_spec_type(st_class: str) -> dict:
    """Returns spectral type of star"""
    st_class = st_class.upper()
    default = "Unknown"

    star_data = {}

    star_data['luminosity'] = get_luminosity(st_class, default)

    return {**star_data, **get_class(st_class, default)}


def get_class(st_class: str, default: str) -> dict:
    """returns star class, class heat and sub class heat 
    if any identifiers are found in the string. Will return
    first istances found
    """
    data = {
        'class': default,
        'heat': default,
        'sub_heat': default
    }

    class_id = get_spectral_class_id(st_class)
    if not class_id:
        return data

    data['class'], data['heat'] = get_class_details(class_id)

    sub_heat = get_sub_class_heat(st_class)
    if not sub_heat:
        return data

    data['sub_heat'] = " ".join([sub_heat, class_id, "type star"])
    return data


def get_spectral_class_id(st_class: str) -> str | None:
    """Return char of class identifier if present"""
    spec_pattern = r"[OBAFGKMLTY]"
    spectral_type = re.search(spec_pattern, st_class)
    if spectral_type:
        return spectral_type.group()
    return None


def get_class_details(class_id: str) -> tuple:
    spectral_classes = {
        'O': ['Blue', '> 30,000'],
        'B': ['Blue-white', '9,700 - 30,000'],
        'A': ['White', '7,200 - 9,700'],
        'F': ['Yellow-white', '5,700 - 7,200'],
        'G': ['Yellow', '4,900 - 5,700'],
        'K': ['Orange', '3,400 - 4,900'],
        'M': ['Red', '2,100 - 3,400'],
        'L': ['Brown dwarf', '1,300 - 2,400'],
        'T': ['Brown dwarf', '< 1,600'],
        'Y': ['Brown dwarf', '< 700']
    }

    star_class = spectral_classes[class_id][0]
    class_heat_range = spectral_classes[class_id][1]

    return star_class, class_heat_range

def get_sub_class_heat(st_class: str) -> str:
    """Return class"""
    sub_class_heat_ranges = {
        "0": "Hottest",
        "1": "Hotter",
        "2": "Hot",
        "3": "High average",
        "4": "Average",
        "5": "Average",
        "6": "Low average",
        "7": "Cool",
        "8": "Cooler",
        "9": "Coolest"
    }

    sub_class = re.search(r"[0-9]", st_class)

    if sub_class:
        return sub_class_heat_ranges[sub_class.group()]
    return None


def get_luminosity(st_class: str, default: str) -> str:
    """
    Look for luminosity identifier in string

    :param str st_class: string to search for luminosity identifier
    :returns str: corresponding luminosity type i.e "white Dwarf"
    """

    luminosity = {
        'IA-O': 'Extremely Luminous Hypergiant',
        'IA': 'Hypergiant',
        'IAB': 'Intermediate Luminous Hypergiant',
        'IB': 'Lesser Hypergiant',
        'II': 'Bright Giant',
        'III': 'Giant',
        'IV': 'Subgiant',
        'V': 'Main Sequence Dwarf',
        'VI': 'Subdwarf',
        'VII': 'White Dwarf'
    }

    item = re.search(r"IA-O|IAB|IA|IB|III|II|IV|VII|VI|V", st_class)
    if item:
        # return the first match item
        return luminosity[item.group()]
    return default
# *******
