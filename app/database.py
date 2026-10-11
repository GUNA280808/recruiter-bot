
import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent.parent / "recruiter.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def create_tables():
    with get_connection() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS candidates (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                experience REAL NOT NULL CHECK (experience >= 0),
                availability TEXT NOT NULL,
                traits TEXT NOT NULL DEFAULT '',
                quirk TEXT NOT NULL DEFAULT ''
            );

            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                min_experience REAL NOT NULL
                    CHECK (min_experience >= 0),
                culture_keywords TEXT NOT NULL DEFAULT '',
                tagline TEXT NOT NULL DEFAULT ''
            );

            CREATE TABLE IF NOT EXISTS candidate_skills (
                candidate_id INTEGER NOT NULL,
                skill TEXT NOT NULL,
                PRIMARY KEY (candidate_id, skill),
                FOREIGN KEY (candidate_id)
                    REFERENCES candidates(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS job_required_skills (
                job_id INTEGER NOT NULL,
                skill TEXT NOT NULL,
                PRIMARY KEY (job_id, skill),
                FOREIGN KEY (job_id)
                    REFERENCES jobs(id) ON DELETE CASCADE
            );
            """
        )
