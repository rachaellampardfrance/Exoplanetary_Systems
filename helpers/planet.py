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
        self._cv_flag = ""
        self._disc_method = ""
        self._disc_instrument = ""
        self._orbit_period = ""
        self._mass = ""
        self._radius = ""
        self._insol_flux = ""
        self._equlib_temp = ""

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
    @property
    def cv_flag(self):
        return self._cv_flag
    @property
    def disc_method(self):
        return self._disc_method
    @property
    def disc_instrument(self):
        return self._disc_instrument
    @property
    def orbit_period(self):
        return self._orbit_period
    @property
    def mass(self):
        return self._mass
    @property
    def radius(self):
        return self._radius
    @property
    def insol_flux(self):
        return self._insol_flux
    @property
    def equlib_temp(self):
        return self._equlib_temp

    def _get_details(self):
        """Gets details of planet by planet name"""
        with sqlite3.connect(Planet.DB) as conn:
            query = f"""
                SELECT disc_pubdate, hostname, cb_flag,
                    declassified, cv_flag, disc_method,
                    disc_instrument, orbit_period, mass,
                    radius, insol_flux, equlib_temp
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
            self._set_cv_flag(details[4])
            self._set_disc_method(details[5])
            self._set_disc_instrument(details[6])
            self._set_orbit_period(details[7])
            self._set_mass(details[8])
            self._set_radius(details[9])
            self._set_insol_flux(details[10])
            self._set_equlib_temp(details[11])

    
    def _set_disc_pubdate(self, pubdate):
        self._disc_pubdate = _get_data_or_default(pubdate)

    def _set_hostname(self, hostname):
        self._hostname = _get_data_or_default(hostname)

    def _set_cb_flag(self, cb_flag):
        self._cb_flag = _get_yes_no(cb_flag)

    def _set_declassified(self, declassified):
        self._declassified = _get_yes_no(declassified)

    def _set_cv_flag(self, cv_flag):
        self._cv_flag = _get_yes_no(cv_flag)
    
    def _set_disc_method(self, disc_method):
        self._disc_method = _get_data_or_default(disc_method)

    def _set_disc_instrument(self, disc_instrument):
        self._disc_instrument = _get_data_or_default(disc_instrument)

    def _set_orbit_period(self, orbit_period):
        self._orbit_period = _get_data_or_default(orbit_period)

    def _set_mass(self, mass):
        self._mass = _get_data_or_default(mass)

    def _set_radius(self, radius):
        self._radius = _get_data_or_default(radius)

    def _set_insol_flux(self, insol_flux):
        self._insol_flux = _get_data_or_default(insol_flux)

    def _set_equlib_temp(self, equlib_temp):
        self._equlib_temp = _get_data_or_default(equlib_temp)


def _get_data_or_default(data):
    if data:
        return data
    else:
        return Planet.DEFAULT

def _get_yes_no(data):
    if data == 1:   
        return "Yes"
    elif data == 0:
        return "No"
    else:
        return Planet.DEFAULT
