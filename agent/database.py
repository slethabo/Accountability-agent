import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).parent.parent / "data" / "accountability.db"


def get_connection():
    return sqlite3.connect(DATABASE_PATH)


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    # Goals table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            goal TEXT NOT NULL,
            completed INTEGER DEFAULT 0,
            due_date TEXT,
            priority INTEGER DEFAULT 3,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tasks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            goal_id INTEGER NOT NULL,
            task TEXT NOT NULL,
            completed INTEGER DEFAULT 0,
            due_date TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (goal_id) REFERENCES goals(id)
        )
    """)

    # Check existing goal columns
    cursor.execute("PRAGMA table_info(goals)")
    goal_columns = [
        column[1]
        for column in cursor.fetchall()
    ]

    # Add due_date to older databases
    if "due_date" not in goal_columns:
        cursor.execute(
            "ALTER TABLE goals ADD COLUMN due_date TEXT"
        )

    # Add priority to older databases
    if "priority" not in goal_columns:
        cursor.execute(
            "ALTER TABLE goals ADD COLUMN priority INTEGER DEFAULT 3"
        )

    # Check existing task columns
    cursor.execute("PRAGMA table_info(tasks)")
    task_columns = [
        column[1]
        for column in cursor.fetchall()
    ]

    # Add due_date to older databases
    if "due_date" not in task_columns:
        cursor.execute(
            "ALTER TABLE tasks ADD COLUMN due_date TEXT"
        )

    connection.commit()
    connection.close()