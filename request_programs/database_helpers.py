"""Helper functions to read collected data into database tables"""

import sqlite3
import pandas as pd

DB_PATH = "database.db"

def upsert_planetary_data(data_frame: pd.DataFrame) -> None:

    """insert/update new pandas dataframe into the planets table"""
    data_to_insert = []
    for _, row in data_frame.iterrows():
        data_to_insert.append((
            row['pl_name'],
            row['hostname'],
            row['sy_snum'],
            row['sy_pnum'],
            row['cb_flag'],
            row['disc_pubdate']
        ))

    with sqlite3.connect(DB_PATH) as connection:
        connection.executemany("""
            INSERT INTO planets (
                pl_name,
                hostname,
                sy_snum,
                sy_pnum,
                cb_flag,
                disc_pubdate,
                last_updated
            )
            VALUES (
                ?, ?, ?, ?, ?, ?, current_timestamp
            )
            ON CONFLICT(pl_name)
            DO UPDATE SET
                hostname = CASE
                    WHEN excluded.hostname != planets.hostname
                    THEN excluded.hostname
                    ELSE planets.hostname END,
                sy_snum = CASE
                    WHEN excluded.sy_snum != planets.sy_snum
                    THEN excluded.sy_snum
                    ELSE planets.sy_snum END,
                sy_pnum = CASE
                    WHEN excluded.sy_pnum != planets.sy_pnum
                    THEN excluded.sy_pnum
                    ELSE planets.sy_pnum END,
                cb_flag = CASE
                    WHEN excluded.cb_flag != planets.cb_flag
                    THEN excluded.cb_flag
                    ELSE planets.cb_flag END,
                last_updated = current_timestamp
            WHERE
                planets.sy_snum != excluded.sy_snum
                OR planets.sy_pnum != excluded.sy_pnum
                OR planets.cb_flag != excluded.cb_flag 
                OR planets.hostname != excluded.hostname;
    """, data_to_insert)


def upsert_systems_data(data_frame: pd.DataFrame) -> None:
    """insert/update new pandas dataframe into the systems table"""
    
    data_to_insert = []
    for _, row in data_frame.iterrows():
        data_to_insert.append((
            row['sy_name'],
            row['sy_snum'],
            row['sy_pnum'],
        ))

    with sqlite3.connect(DB_PATH) as connection:
        connection.executemany("""
            INSERT INTO systems (
                sy_name,
                sy_snum,
                sy_pnum,
                last_updated
            )
            VALUES (
                ?, ?, ?, current_timestamp
            )
            ON CONFLICT(sy_name)
            DO UPDATE SET
                sy_name = CASE
                    WHEN excluded.sy_name != systems.sy_name
                    THEN excluded.sy_name
                    ELSE systems.sy_name END,
                sy_snum = CASE
                    WHEN excluded.sy_snum != systems.sy_snum
                    THEN excluded.sy_snum
                    ELSE systems.sy_snum END,
                sy_pnum = CASE
                    WHEN excluded.sy_pnum != systems.sy_pnum
                    THEN excluded.sy_pnum
                    ELSE systems.sy_pnum END,
                last_updated = current_timestamp
            WHERE
                systems.sy_snum != excluded.sy_snum
                OR systems.sy_pnum != excluded.sy_pnum;
    """, data_to_insert)


def upsert_stellar_data(data_frame: pd.DataFrame) -> None:
    """insert/update new pandas dataframe into the systems table"""
    
    data_to_insert = []
    for _, row in data_frame.iterrows():
        data_to_insert.append((
            row['sy_name'],
            row['hostname'],
        ))

    with sqlite3.connect(DB_PATH) as connection:
        connection.executemany("""
            INSERT INTO stellar (
                sy_name,
                hostname,
                last_updated
            )
            VALUES (
                ?, ?, current_timestamp
            )
            ON CONFLICT(hostname)
            DO UPDATE SET
                sy_name = CASE
                    WHEN excluded.sy_name != stellar.sy_name
                    THEN excluded.sy_name
                    ELSE stellar.sy_name END,
                last_updated = current_timestamp
            WHERE
                stellar.sy_name != excluded.sy_name;
    """, data_to_insert)

def update_stellar_spectypes(data_frame: pd.DataFrame) -> None:
    """update stellar table with new spectral types"""

    data_to_insert = []
    for _, row in data_frame.iterrows():
        data_to_insert.append((
            row['st_spectype'],
            row['hostname'],
        ))

    with sqlite3.connect(DB_PATH) as connection:
        connection.executemany("""
            UPDATE stellar
            SET st_spectype = ?
            WHERE
                stellar.hostname == ?;
    """, data_to_insert)


def get_last_updated(table) -> str:
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()

        c.execute("""
            SELECT MAX(last_updated)
            FROM {}
        """.format(table))

        return c.fetchone()

 
def get_systems_db_data():
    with sqlite3.connect(DB_PATH) as conn:
        # c = conn.cursor()
        
        return pd.read_sql_query("SELECT * FROM systems", conn)

def print_table_updated_count(table: str) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()

        today = c.execute("SELECT DATE('now')").fetchone()[0]

        c.execute(f"""
            SELECT COUNT(*)
            FROM {table}
            WHERE DATE(last_updated) = '{today}';
        """)

        result = c.fetchone()
        count = result[0] if result else 0

        print(f"New updates to {table}: {count}")