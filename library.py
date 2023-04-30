import tkinter as tk
import tkinter.ttk as ttk
import sqlite3

# Connect to the database
conn = sqlite3.connect('library.db')
c = conn.cursor()

# Create the books table if it doesn't already exist
c.execute('''CREATE TABLE IF NOT EXISTS books
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              title TEXT,
              author TEXT,
              isbn TEXT)''')

class LibraryApp:
    def _init_(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.create_widgets()
        self.populate_table()

    def create_widgets(self):
        # Create a label for the title
        title_label = tk.Label(self.root, text="Library Management System", font=("Arial", 24))
        title_label.pack(pady=20)

        # Create input fields for adding new books
        self.title_entry = tk.Entry(self.root, width=50)
        self.title_entry.pack()
        self.author_entry = tk.Entry(self.root, width=50)
        self.author_entry.pack()
        self.isbn_entry = tk.Entry(self.root, width=50)
        self.isbn_entry.pack()

        # Create a button for adding new books
        add_button = tk.Button(self.root, text="Add Book", command=self.add_book)
        add_button.pack(pady=10)

        # Create a table for displaying existing books
        table_frame = tk.Frame(self.root)
        table_frame.pack(pady=20)
        table_columns = ("ID", "Title", "Author", "ISBN")
        self.table = tk.ttk.Treeview(table_frame, columns=table_columns, show="headings")
        for col in table_columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=100)
        self.table.pack()

    def add_book(self):
        # Get input values
        title = self.title_entry.get()
        author = self.author_entry.get()
        isbn = self.isbn_entry.get()

        # Insert values into the database
        c.execute("INSERT INTO books (title, author, isbn) VALUES (?, ?, ?)", (title, author, isbn))
        conn.commit()

        # Clear input fields
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.isbn_entry.delete(0, tk.END)

        # Update the table with the new data
        self.populate_table()

    def populate_table(self):
        # Clear the existing data from the table
        for row in self.table.get_children():
            self.table.delete(row)

        # Get the data from the database and populate the table
        c.execute("SELECT * FROM books")
        rows = c.fetchall()
        for row in rows:
            self.table.insert("", tk.END, values=row)

# Create the main window
root = tk.Tk()
app = LibraryApp(root)
root.mainloop()

# Close the database connection when the program exits
conn.close()