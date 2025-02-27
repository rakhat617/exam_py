import sqlite3

def create_jobs_db():
        conn = sqlite3.connect('jobs.db')

        conn.execute("""
                CREATE TABLE IF NOT EXISTS jobs(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                title TEXT NOT NULL,
                experience TEXT NOT NULL,
                employment TEXT NOT NULL,
                format TEXT NOT NULL,
                city TEXT NOT NULL,     
                description TEXT NOT NULL,
                salary TEXT NOT NULL
                )
        """)

        conn.commit()
        conn.close()

def create_users_db():
        conn = sqlite3.connect('users.db')

        conn.execute("""
                CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                name TEXT NOT NULL,
                surname TEXT NOT NULL,
                image TEXT
                )
        """)

        conn.commit()
        conn.close()