import sqlite3
from typing import List, Tuple

# Constants for better maintainability
DB_NAME = 'python_programming.db'
TABLE_NAME = 'python_programming'

def connect_db(db_name: str) -> sqlite3.Connection:
    """Connect to the SQLite database."""
    return sqlite3.connect(db_name)

def create_table(cursor: sqlite3.Cursor, table_name: str) -> None:
    """Create the table if it doesn't exist."""
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            grade INTEGER CHECK(grade >= 0 AND grade <= 100)
        )
    ''')

def insert_students(cursor: sqlite3.Cursor, table_name: str, students: List[Tuple[int, str, int]]) -> None:
    """Insert multiple students into the table."""
    cursor.executemany(f'''
        INSERT OR IGNORE INTO {table_name} (id, name, grade)
        VALUES (?, ?, ?)
    ''', students)

def select_students_by_grade(cursor: sqlite3.Cursor, table_name: str, min_grade: int, max_grade: int) -> List[Tuple]:
    """Select students with grade between min and max."""
    cursor.execute(f'''
        SELECT * FROM {table_name}
        WHERE grade BETWEEN ? AND ?
    ''', (min_grade, max_grade))
    return cursor.fetchall()

def update_student_grade(cursor: sqlite3.Cursor, table_name: str, name: str, new_grade: int) -> int:
    """Update a student's grade by name. Returns number of rows affected."""
    cursor.execute(f'''
        UPDATE {table_name}
        SET grade = ?
        WHERE name = ?
    ''', (new_grade, name))
    return cursor.rowcount

def delete_student(cursor: sqlite3.Cursor, table_name: str, name: str) -> int:
    """Delete a student by name. Returns number of rows affected."""
    cursor.execute(f'''
        DELETE FROM {table_name}
        WHERE name = ?
    ''', (name,))
    return cursor.rowcount

def update_grades_by_id(cursor: sqlite3.Cursor, table_name: str, id_threshold: int, new_grade: int) -> int:
    """Update grades for students with id > threshold. Returns number of rows affected."""
    cursor.execute(f'''
        UPDATE {table_name}
        SET grade = ?
        WHERE id > ?
    ''', (new_grade, id_threshold))
    return cursor.rowcount

def main():
    """Main function to perform database operations."""
    students = [
        (55, 'Sethu Hana', 61),
        (66, 'Dennis Fredrickson', 88),
        (77, 'Lilly April', 78),
        (12, 'Peyton Sawyer', 45),
        (2, 'Lucas Brooke', 99)
    ]

    try:
        with connect_db(DB_NAME) as db:
            cursor = db.cursor()

            # Create table
            create_table(cursor, TABLE_NAME)

            # Insert data
            insert_students(cursor, TABLE_NAME, students)

            # Select and print students with grade between 60 and 80
            results = select_students_by_grade(cursor, TABLE_NAME, 60, 80)
            print("Students with grade between 60 and 80:")
            for row in results:
                print(row)

            # Update Sethu Hana's grade
            updated = update_student_grade(cursor, TABLE_NAME, 'Sethu Hana', 65)
            if updated == 0:
                print("Warning: No student named 'Sethu Hana' found to update.")

            # Delete Dennis Fredrickson's row
            deleted = delete_student(cursor, TABLE_NAME, 'Dennis Fredrickson')
            if deleted == 0:
                print("Warning: No student named 'Dennis Fredrickson' found to delete.")

            # Update grades for id > 55
            updated_bulk = update_grades_by_id(cursor, TABLE_NAME, 55, 80)
            print(f"Updated grades for {updated_bulk} students with id > 55.")

            # Commit all changes
            db.commit()

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()