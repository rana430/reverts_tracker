import sqlite3

connection = sqlite3.connect("revertdp.db")
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

cursor.execute(
    """
    CREATE TABLE "meetings" (
	"id"	INTEGER NOT NULL UNIQUE,
	"meeting-id"	INTEGER NOT NULL UNIQUE,
	"date"	DATE NOT NULL,
	"state"	TEXT NOT NULL,
	"notes"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
    """
)

cursor.execute(
    """
CREATE TABLE "attendees" (
    "id" INTEGER NOT NULL UNIQUE,
    "name" TEXT NOT NULL,
    "meeting_id" INTEGER NOT NULL,
    PRIMARY KEY("id" AUTOINCREMENT),
    FOREIGN KEY("meeting_id") REFERENCES "meetings"("id")
);

"""
)
connection.commit()
connection.close()


# /add user drop table
