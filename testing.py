import sqlite3    

db = "database.db"

with sqlite3.connect(db) as conn:
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM planetary_systems
        WHERE hostname = (
            SELECT sy_name
            FROM stellar_hosts
            WHERE sy_name = 'Kepler-158')
    """)
    rows = cursor.fetchall()

    for row in rows:
        print(row)