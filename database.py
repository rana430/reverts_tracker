import sqlite3

connection = sqlite3.connect("db/reverts_database.db")
cursor = connection.cursor()
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS REVERTS (
        id INTEGER PRIMARY KEY,
        revert_id INTEGER NOT NULL,
        gender TEXT NOT NULL,
        mod_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        notes TEXT
    );
"""
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS HISTORY (
        id INTEGER PRIMARY KEY,
        revert_id INTEGER NOT NULL,
        mod_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        notes TEXT,
        FOREIGN KEY (revert_id) REFERENCES REVERTS (revert_id),
        FOREIGN KEY (mod_id) REFERENCES REVERTS (mod_id)
    );
"""
)

connection.commit()
connection.close()
