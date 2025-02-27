import sqlite3

def create_jobs_db():
        conn = sqlite3.connect('jobs.db')

        conn.execute("""
                CREATE TABLE IF NOT EXISTS jobs(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL UNIQUE,
                experience TEXT NOT NULL UNIQUE,
                employment TEXT NOT NULL UNIQUE,
                format TEXT NOT NULL UNIQUE,
                city TEXT NOT NULL UNIQUE,     
                description TEXT NOT NULL UNIQUE,
                salary TEXT NOT NULL UNIQUE
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
                name TEXT NOT NULL UNIQUE,
                surname TEXT NOT NULL UNIQUE
                )
        """)

        conn.commit()
        conn.close()