import re
import sqlite3

class Planet():
    DB = "database.db"
    DEFAULT = "Unknown"
    def __init__(self, planet_name: str):
        self.name = planet_name

        self._disc_pubdate = ""
        self._hostname = ""
        self._cb_flag = ""
        self._declassified = ""

        self._get_details()

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, planet_name:str):
        self._name = planet_name

    @property
    def disc_pubdate(self):
        return self._disc_pubdate
    @property
    def hostname(self):
        return self._hostname
    @property
    def cb_flag(self):
        return self._cb_flag
    @property
    def declassified(self):
        return self._declassified

    def _get_details(self):
        """Gets details of planet by planet name"""
        with sqlite3.connect(Planet.DB) as conn:
            query = f"""
                SELECT disc_pubdate, hostname, cb_flag, declassified
                FROM planets
                WHERE pl_name=?;
            """
            cursor = conn.cursor()
            cursor.execute(query, (self.name,))
            details = cursor.fetchone()

            self._set_disc_pubdate(details[0])
            self._set_hostname(details[1])
            self._set_cb_flag(details[2])
            self._set_declassified(details[3])

    
    def _set_disc_pubdate(self, pubdate):
        if pubdate:
            self._disc_pubdate = pubdate
        else:
            self._disc_pubdate = Planet.DEFAULT

    def _set_hostname(self, hostname):
        if hostname:
            self._hostname = hostname
        else:
            self._hostname = Planet.DEFAULT

    def _set_cb_flag(self, cb_flag):

        if cb_flag == 1:
            self._cb_flag = "Yes"
        elif cb_flag == 0:
            self._cb_flag = "No"
        else:
            self._cb_flag = Planet.DEFAULT

    def _set_declassified(self, declassified):

        if declassified == 1:
            self._declassified = "Yes"
        elif declassified == 0:
            self._declassified = "No"
        else:
            self._declassified = Planet.DEFAULT
    