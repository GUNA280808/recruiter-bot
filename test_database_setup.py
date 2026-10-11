
import sqlite3

from app.database import DATABASE_PATH, create_tables, get_connection

create_tables()

with get_connection() as connection:
    tables = connection.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name
        """
    ).fetchall()

    print("Database path:", DATABASE_PATH)
    print("Tables created:")

    for table in tables:
        print("-", table["name"])

print("Database setup successful!")
