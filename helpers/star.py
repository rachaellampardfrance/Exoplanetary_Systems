"""Class holds all assumed star types"""
import re
import sqlite3

from helpers.planet import Planet

class Star():
    DB = "database.db"
    TABLES = ['planets', 'systems', 'stars']
    SPECTRAL_CLASSES = {
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
    SUBCLASS_HEAT = {
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
    LUMINOSITY = {
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
    DEFAULT = "Unknown"

    def __init__(self, name:str, system:str =None):
        self.name = name
        self._planets: list = []

        self._system = ""
        self._full_class_id = "" # "G2 III"
        self._class_id = "" # "G"
        self._st_class = "" # "Yellow"
        self._heat = "" # "4,900 - 5,700"
        self._sub_class = "" # "Average G type star"
        self._lumin = "" # "Giant"

        self._get_full_class_id()
        self._get_details(system)
        self._generate_planets()

    # used for checking equality in a set
    def __hash__(self):
        return hash(self.name)
    def __eq__(self, other):
        if isinstance(other, Star):
            return self.name == other.name
        return False
    
    def __repr__(self):
        return f"Star(name={self.name})"

    @property
    def name(self) -> str:
        return self._name
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def system(self) -> str:
        return self._system
    @property
    def full_class_id(self) -> str:
        return self._full_class_id
    @property
    def class_id(self) -> str:
        return self._class_id
    @property
    def st_class(self) -> str:
        return self._st_class
    @property
    def heat(self) -> str:
        return self._heat
    @property
    def sub_class(self) -> str:
        return self._sub_class
    @property
    def lumin(self) -> str:
        return self._lumin

    def _get_full_class_id(self):
        """find star spectral type from database using star name
        (hostname) and using passed in database connection"""
        with sqlite3.connect(Star.DB) as conn:
            cursor = conn.cursor()
            query = f"""
                SELECT st_spectype
                FROM stars
                WHERE hostname=?;
            """
            cursor.execute(query, (self.name,))
            full_class = cursor.fetchone()

            if full_class[0]:
                self._full_class_id = full_class[0]
            else:
                self._full_class_id = Star.DEFAULT

            cursor.close()

    def _get_details(self, system:str =None) -> None:
        """set star all instance variables"""
        self._set_system(system)

        if self.full_class_id == Star.DEFAULT:
            return
        
        self._set_class_id()
        self._set_st_class()
        self._set_heat()
        self._set_sub_class()
        self._set_lumin()

    def _set_system(self, system:str =None) -> None:
        if not system == None:
            self._system = system
        else:
            self._set_system_from_star()

    def _set_system_from_star(self):
        """try search table for system name using hostname"""
        with sqlite3.connect(Star.DB) as conn:
            cursor = conn.cursor()
            query = f"""
                SELECT sy_name
                FROM {Star.TABLES[2]}
                WHERE LOWER(hostname)=?;
            """
            cursor.execute(query, (self.name.lower(),))

            self._system = cursor.fetchone()[0]

    def _set_class_id(self) -> None:
        """Return char of class identifier if present"""
        spec_pattern = r"[OBAFGKMLTY]"
        spectral_type = re.search(spec_pattern, self.full_class_id)
        if spectral_type:
            self._class_id = spectral_type.group()
        else:
            self._class_id = Star.DEFAULT

    def _set_st_class(self) -> None:
        """sets st_class by class_id if exists"""
        if self.class_id == Star.DEFAULT:
            self._st_class = Star.DEFAULT
            return
        self._st_class = Star.SPECTRAL_CLASSES[self.class_id][0]

    def _set_heat(self) -> None:
        """sets st_heat by class_id if exists"""
        if self.class_id == Star.DEFAULT:
            self._heat = Star.DEFAULT
            return
        self._heat = Star.SPECTRAL_CLASSES[self.class_id][1]

    def _set_sub_class(self) -> None:
        sub_class = re.search(r"[0-9]", self.full_class_id)

        if sub_class:
            text = f" {self.class_id} type star"
            self._sub_class = Star.SUBCLASS_HEAT[sub_class.group()] + text
        else:
            self._sub_class = Star.DEFAULT

    def _set_lumin(self) -> None:
        lumin = re.search(r"IA-O|IAB|IA|IB|III|II|IV|VII|VI|V", self.full_class_id)
        if lumin:
            # return the first match item
            self._lumin = Star.LUMINOSITY[lumin.group()]
        else:
            self._lumin = Star.DEFAULT


# Set: system.planets
# *****************************
    @property
    def planets(self) -> list:
        return self._planets
    
    def _generate_planets(self):
        """Generate planets by stars from self.stars"""
        planets = []
        with sqlite3.connect(Star.DB) as conn:
            cursor = conn.cursor()

            query = f"""
                SELECT pl_name
                FROM {Star.TABLES[0]}
                WHERE hostname=?;
            """
            cursor.execute(query, (self.name,))
            results = cursor.fetchall()

            for result in results:
                planets.append(result[0])

            cursor.close()

            # raise TypeError(f"planets = {planets}")

        for planet in planets:
            planet_details = Planet(planet, system=self.system)
            self._planets.append(planet_details)
# *****************************
