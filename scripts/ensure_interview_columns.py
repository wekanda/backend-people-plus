import sqlite3

DB = 'people_pluse.db'
cols_to_add = [
    ("candidate_name", "VARCHAR"),
    ("position", "VARCHAR"),
    ("interviewer", "VARCHAR"),
    ("notes", "TEXT")
]

conn = sqlite3.connect(DB)
c = conn.cursor()

c.execute("PRAGMA table_info(interviews)")
existing = [row[1] for row in c.fetchall()]

for name, coltype in cols_to_add:
    if name not in existing:
        try:
            c.execute(f"ALTER TABLE interviews ADD COLUMN {name} {coltype}")
            print(f"Added column {name} {coltype}")
        except Exception as e:
            print(f"Failed to add {name}: {e}")
    else:
        print(f"Column {name} already exists")

conn.commit()
conn.close()
