"""
Bookstore Management System - shelf_track.py

This program allows a bookstore clerk to manage book inventory.
Features include adding, updating, deleting, and searching books,
as well as viewing detailed book information with author details.

Database: ebookstore.db
Tables: book (id, title, authorID, qty), author (id, name, country)
"""

import sqlite3

# Database setup
DB_NAME = 'ebookstore.db'

def create_tables():
    """Create the book and author tables if they don't exist."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        # Create book table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS book (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                authorID INTEGER NOT NULL,
                qty INTEGER NOT NULL
            )
        ''')

        # Create author table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS author (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                country TEXT NOT NULL
            )
        ''')

        conn.commit()

def populate_initial_data():
    """Populate the tables with initial data."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        # Populate book table
        books = [
            (3001, 'A Tale of Two Cities', 1290, 30),
            (3002, 'Harry Potter and the Philosopher\'s Stone', 8937, 40),
            (3003, 'The Lion, the Witch and the Wardrobe', 2356, 25),
            (3004, 'The Lord of the Rings', 6380, 37),
            (3005, 'Alice\'s Adventures in Wonderland', 5620, 12)
        ]

        cursor.executemany('''
            INSERT OR IGNORE INTO book (id, title, authorID, qty)
            VALUES (?, ?, ?, ?)
        ''', books)

        # Populate author table
        authors = [
            (1290, 'Charles Dickens', 'England'),
            (8937, 'J.K. Rowling', 'England'),
            (2356, 'C.S. Lewis', 'Ireland'),
            (6380, 'J.R.R. Tolkien', 'South Africa'),
            (5620, 'Lewis Carroll', 'England')
        ]

        cursor.executemany('''
            INSERT OR IGNORE INTO author (id, name, country)
            VALUES (?, ?, ?)
        ''', authors)

        conn.commit()

def add_book():
    """Add a new book to the database."""
    try:
        id = int(input("Enter book ID (4 digits): "))
        if len(str(id)) != 4:
            print("Book ID must be exactly 4 digits.")
            return
        title = input("Enter book title: ")
        authorID = int(input("Enter author ID (4 digits): "))
        if len(str(authorID)) != 4:
            print("Author ID must be exactly 4 digits.")
            return
        qty = int(input("Enter quantity: "))
        if qty < 0:
            print("Quantity cannot be negative.")
            return

        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO book (id, title, authorID, qty)
                VALUES (?, ?, ?, ?)
            ''', (id, title, authorID, qty))
            conn.commit()
            print("Book added successfully.")
    except ValueError:
        print("Invalid input. Please enter numbers where required.")
    except sqlite3.IntegrityError:
        print("Book ID already exists.")

def update_book():
    """Update book information."""
    try:
        id = int(input("Enter book ID to update: "))
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM book WHERE id = ?', (id,))
            book = cursor.fetchone()
            if not book:
                print("Book not found.")
                return
            print(f"Current: ID: {book[0]}, Title: {book[1]}, AuthorID: {book[2]}, Qty: {book[3]}")

            print("What to update? 1. Quantity (default), 2. Title, 3. AuthorID")
            choice = input("Enter choice (1-3): ").strip()
            if choice == '2':
                new_title = input("Enter new title: ")
                cursor.execute('UPDATE book SET title = ? WHERE id = ?', (new_title, id))
            elif choice == '3':
                new_authorID = int(input("Enter new authorID: "))
                cursor.execute('UPDATE book SET authorID = ? WHERE id = ?', (new_authorID, id))
            else:
                new_qty = int(input("Enter new quantity: "))
                cursor.execute('UPDATE book SET qty = ? WHERE id = ?', (new_qty, id))
            conn.commit()
            print("Book updated successfully.")
    except ValueError:
        print("Invalid input.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def delete_book():
    """Delete a book from the database."""
    try:
        id = int(input("Enter book ID to delete: "))
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM book WHERE id = ?', (id,))
            if cursor.rowcount == 0:
                print("Book not found.")
            else:
                conn.commit()
                print("Book deleted successfully.")
    except ValueError:
        print("Invalid book ID.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def search_books():
    """Search for books by title or ID."""
    search_term = input("Enter book title or ID to search: ").strip()
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM book
            WHERE title LIKE ? OR id = ?
        ''', (f'%{search_term}%', search_term))
        results = cursor.fetchall()
        if results:
            print("Search results:")
            for row in results:
                print(f"ID: {row[0]}, Title: {row[1]}, AuthorID: {row[2]}, Qty: {row[3]}")
        else:
            print("No books found.")

def view_all_books():
    """View details of all books with author info."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT book.title, author.name, author.country
            FROM book
            INNER JOIN author ON book.authorID = author.id
            ORDER BY book.id
        ''')
        results = cursor.fetchall()
        print("Details")
        print("-" * 50)
        for title, name, country in results:
            print(f"Title: {title}")
            print(f"Author's Name: {name}")
            print(f"Author's Country: {country}")
            print("-" * 50)

def update_book_with_author():
    """Update book and author information."""
    try:
        id = int(input("Enter book ID to update: "))
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT book.title, author.name, author.country
                FROM book
                INNER JOIN author ON book.authorID = author.id
                WHERE book.id = ?
            ''', (id,))
            result = cursor.fetchone()
            if not result:
                print("Book not found.")
                return
            title, author_name, author_country = result
            print(f"Current Title: {title}")
            print(f"Author's Name: {author_name}")
            print(f"Author's Country: {author_country}")

            new_name = input("Enter new author's name (leave blank to keep): ").strip()
            new_country = input("Enter new author's country (leave blank to keep): ").strip()

            if new_name:
                cursor.execute('UPDATE author SET name = ? WHERE id = (SELECT authorID FROM book WHERE id = ?)', (new_name, id))
            if new_country:
                cursor.execute('UPDATE author SET country = ? WHERE id = (SELECT authorID FROM book WHERE id = ?)', (new_country, id))

            conn.commit()
            print("Author information updated successfully.")
    except ValueError:
        print("Invalid input.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def menu():
    """Display the menu and handle user choices."""
    while True:
        print("\nMenu:")
        print("1. Enter book")
        print("2. Update book")
        print("3. Delete book")
        print("4. Search books")
        print("5. View details of all books")
        print("0. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            add_book()
        elif choice == '2':
            update_book_with_author()  # Updated for Part 2
        elif choice == '3':
            delete_book()
        elif choice == '4':
            search_books()
        elif choice == '5':
            view_all_books()
        elif choice == '0':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    create_tables()
    populate_initial_data()
    menu()