import sqlite3

# Establish connection to the database
db = sqlite3.connect('ebookstore.db')
cursor = db.cursor()

# Create the 'book' table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS book(
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        qty INTEGER NOT NULL
    )
''')

# Seed initial data into the 'book' table
book_info = [
    (3001, "A Tale of Two Cities", "Charles Dickens", 30),
    (3002, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40),
    (3003, "The Lion, the Witch and the Wardrobe", "C.S. Lewis", 25),
    (3004, "The Lord of the Rings", "J.R.R. Tolkien", 37),
    (3005, "Alice in Wonderland", "Lewis Carroll", 12)
]

cursor.executemany('''
    INSERT OR IGNORE INTO book (id, title, author, qty) 
    VALUES (?, ?, ?, ?)
''', book_info)
db.commit()


# Function to enter a new book
def enter_book():
    print("Hi! Please type in the necessary info to enter a book.")
    try:
        book_id = int(input("Please enter the ID: "))
        cursor.execute('SELECT id FROM book WHERE id = ?', (book_id,))
        if cursor.fetchone():
            print("A book with this ID already exists. Please enter a different ID.")
            return enter_book()

        book_title = input("Please enter the title: ")
        book_author = input("Please enter the author's name: ")
        book_qty = int(input("Please enter the quantity: "))

        cursor.execute('''
            INSERT INTO book (id, title, author, qty) 
            VALUES (?, ?, ?, ?)
        ''', (book_id, book_title, book_author, book_qty))
        db.commit()
        print("Book entered successfully!")
    except ValueError:
        print("Invalid input. Please enter numeric values for ID and quantity.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")


# Function to update book details
def update_book():
    print("Hi! Please type in the ID of the book you want to update.")
    try:
        book_id = int(input("Book ID: "))
        cursor.execute('SELECT * FROM book WHERE id = ?', (book_id,))
        if not cursor.fetchone():
            print("Book not found. Please enter a valid ID.")
            return

        while True:
            user_update = input('''1. Book Title
2. Author's Name
3. Book Quantity
Which part of the book do you want to update? ''')

            if user_update == '1':
                book_title = input("Please type in the new title: ")
                cursor.execute('''
                    UPDATE book SET title = ? WHERE id = ?
                ''', (book_title, book_id))
                print("Book title updated successfully!")

            elif user_update == '2':
                book_author = input("Please type in the new author's name: ")
                cursor.execute('''
                    UPDATE book SET author = ? WHERE id = ?
                ''', (book_author, book_id))
                print("Author's name updated successfully!")

            elif user_update == '3':
                book_qty = int(input("Please type in the new quantity amount: "))
                cursor.execute('''
                    UPDATE book SET qty = ? WHERE id = ?
                ''', (book_qty, book_id))
                print("Book quantity updated successfully!")

            else:
                print("Please enter a valid option (1, 2, 3).")
                continue

            db.commit()
            if input("Would you like to keep updating? (yes/no): ").lower() != "yes":
                break

    except ValueError:
        print("Invalid input. Please enter a numeric value for the ID.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")


# Function to delete a book
def delete_book():
    print("Hi! Please type in the ID of the book you want to delete.")
    try:
        book_id = int(input("Please enter the ID of the book you want to delete: "))
        cursor.execute('SELECT * FROM book WHERE id = ?', (book_id,))
        if not cursor.fetchone():
            print("Book not found. Please enter a valid ID.")
            return

        if input(f"Are you sure you want to delete book {book_id}? (yes/no): ").lower() == "yes":
            cursor.execute('DELETE FROM book WHERE id = ?', (book_id,))
            db.commit()
            print("Book deleted successfully!")
        else:
            print("Deletion cancelled.")

    except ValueError:
        print("Invalid input. Please enter a numeric value for the ID.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")


# Function to search for a book
def search_book():
    try:
        cursor.execute('SELECT * FROM book')
        books = cursor.fetchall()
        if books:
            print("Current books in the database:")
            for book in books:
                print(book)
        else:
            print("No books available in the database.")

        id_title = input("Would you like to search the book by its ID or by its TITLE? ").lower()
        if id_title == "id":
            id_num = int(input("Please enter the ID number of the book: "))
            cursor.execute('SELECT * FROM book WHERE id = ?', (id_num,))
        elif id_title == "title":
            title_name = input("Please enter the title of the book: ")
            cursor.execute('SELECT * FROM book WHERE title = ?', (title_name,))
        else:
            print("Invalid entry, please try again.")
            return search_book()

        result = cursor.fetchone()
        if result:
            print(result)
        else:
            print("Book not found.")

    except ValueError:
        print("Invalid input. Please enter a numeric value for the ID.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")


# User interface loop
while True:
    user_selection = input('''1. Enter Book
2. Update Book
3. Delete Book
4. Search Book
0. Exit
: ''')
    if user_selection == "1":
        enter_book()
    elif user_selection == "2":
        update_book()
    elif user_selection == "3":
        delete_book()
    elif user_selection == "4":
        search_book()
    elif user_selection == "0":
        print("Goodbye!")
        break
    else:
        print("Please enter a valid option (1, 2, 3, 4, 0).")

# Close the database connection
db.close()
