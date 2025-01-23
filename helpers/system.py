"""System class for system information"""
import sqlite3
from helpers.star import Star
from helpers.planet import Planet

class System():
    """Class returns object of system when initialised with valid stellar body"""
    DB = "database.db"
    TABLES = ['planets', 'systems', 'stellar']

    def __init__(self, stellar_body):
        self._name: str = None
        self._stars: list = []
        self._planets: list = []

        self.name: str = stellar_body
        self._generate_stars()
        self._generate_planets()


# Set system.name
# *****************************
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, stellar_body):
        # stellar_body = stellar_body.lower()
        with sqlite3.connect(System.DB) as con:
            cursor = con.cursor()

            try:
                host = self._try_host_from_planet(stellar_body, cursor)
                self._name = self._try_system_from_host(host, cursor)
                return

            except TypeError:
                try:
                    self._name = self._try_system_from_host(stellar_body, cursor)
                    return

                except TypeError:
                    self._name = self._try_system(stellar_body, cursor)


    def _try_host_from_planet(self, stellar_body: str, cursor: sqlite3.Cursor) -> str:
        """try search table for system name using hostname"""
        query = f"""
            SELECT hostname
              FROM {System.TABLES[0]}
             WHERE LOWER(pl_name)=?;
        """
        cursor.execute(query, (stellar_body.lower(),))

        return cursor.fetchone()[0]


    def _try_system_from_host(self, stellar_body: str, cursor: sqlite3.Cursor) -> str:
        """try search table for system name using hostname"""
        query = f"""
            SELECT sy_name
              FROM {System.TABLES[2]}
             WHERE LOWER(hostname)=?;
        """
        cursor.execute(query, (stellar_body.lower(),))

        return cursor.fetchone()[0]


    def _try_system(self, stellar_body: str, cursor: sqlite3.Cursor) -> str:
        """try search directly for system name"""
        query = f"""
            SELECT sy_name
              FROM {System.TABLES[1]}
             WHERE LOWER(sy_name)=?;
        """
        cursor.execute(query, (stellar_body.lower(),))

        return cursor.fetchone()[0]
# *****************************


# Set: system.stars
# *****************************
    @property
    def stars(self) -> list:
        return self._stars
    
    def _generate_stars(self):
        """Generate stars in system from self.name (system name)"""
        with sqlite3.connect(System.DB) as conn:
            cursor = conn.cursor()

            query = f"""
                SELECT hostname
                FROM {System.TABLES[2]}
                WHERE sy_name=?;
            """
            cursor.execute(query, (self.name,))
            stars = cursor.fetchall()
            cursor.close()

            for star in stars:
                star_details = Star(star[0], conn)
                self._stars.append(star_details)
# *****************************


# Set: system.planets
# *****************************
    @property
    def planets(self) -> list:
        return self._planets
    
    def _generate_planets(self):
        """Generate planets by stars from self.stars"""
        with sqlite3.connect(System.DB) as conn:
            planets = []

            for star in self.stars:
                cursor = conn.cursor()
                query = f"""
                    SELECT pl_name
                    FROM {System.TABLES[0]}
                    WHERE hostname=?;
                """
                cursor.execute(query, (star.name,))
                results = cursor.fetchall()

                for result in results:
                    planets.append(result[0])

                cursor.close()

            # raise TypeError(f"planets = {planets}")

            for planet in planets:
                planet_details = Planet(planet, conn)
                self._planets.append(planet_details)
# *****************************
