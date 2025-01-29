import re
import sqlite3

class Planet():
    DEFAULT = "Unknown"
    def __init__(self, planet_name: str, conn: sqlite3.Connection):
        self.name = planet_name

        self._disc_pubdate = ""
        self._hostname = ""
        self._cb_flag = ""

        self._get_details(conn)

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

    def _get_details(self, conn):
        """Gets details of planet by planet name"""
        query = f"""
            SELECT disc_pubdate, hostname, cb_flag
              FROM planetary_systems
             WHERE pl_name=?;
        """
        cursor = conn.cursor()
        cursor.execute(query, (self.name,))
        details = cursor.fetchone()

        self._set_disc_pubdate(details[0])
        self._set_hostname(details[1])
        self._set_cb_flag(details[2])

    
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
    