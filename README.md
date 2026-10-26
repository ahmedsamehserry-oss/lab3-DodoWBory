# Database Lab 3

This is our Database Lab 3 project using MySQL, Python, and Flask.

The lab has two problems. In Problem 1, we created a company database and tested foreign keys. In Problem 2, we created a library database and added books and authors to our previous Lab 2 website.

## Problem 1 - Company Database

We created a database called `company` with three tables:

- `EMPLOYEE` - stores employee information.
- `DEPARTMENT` - stores department information and managers.
- `PROJECT` - stores projects and their departments.

We used primary keys and foreign keys to connect the tables.

We also inserted at least 3 records into each table and tested what happens when we try to insert or delete records that break foreign key rules.

The SQL commands and results for questions Q1.1, Q1.2, and Q1.3 are in `problem1_Answers.txt`.

## Problem 2 - Library Database

We created another database called `library` with two tables:

- `AUTHOR` - author ID, name, country, and photo.
- `BOOK` - book ID, title, price, author ID, and cover image.

Each book belongs to an author using `author_id` as a foreign key.

We used `ON DELETE CASCADE`, so deleting an author also deletes their books.

The database starts with at least 3 authors and 6 books.

## Website

We continued our Lab 2 To-Do List website and added a Library page.

The website includes:

- Register, Login, and Logout.
- Personal To-Do List with Add, Edit, Done/Undo, and Delete.
- Task counters for total, completed, and open tasks.
- Display all authors and books.
- Add, edit, and delete authors.
- Add, edit, and delete books.
- Form validation and user sessions.

We used HTML, CSS, and JavaScript for the frontend, Python and Flask for the backend, and MySQL for storing the data.

## Bonus - Book Covers and Author Photos

We also added the image upload bonus.

Users can upload a photo for an author or a cover image for a book when adding or editing records.

The website accepts JPG, PNG, WEBP, and GIF images, with a maximum upload size of 3 MB per image.

Uploaded images are converted to WEBP and saved in:

- `website/static/uploads/authors/`
- `website/static/uploads/books/`

The image filenames are stored in MySQL, and the pictures are displayed in the Library tables.

## How to Run the Project

### 1. Set up MySQL

Open MySQL Workbench and run these files in order:

For Problem 1:

1. `problem1_DDL.sql`
2. `problem1_DML.sql`

For Problem 2:

1. `problem2_DDL.sql`
2. `problem2_DML.sql`

The DDL files create the databases and tables. The DML files insert the sample data.

**Note:** The DDL scripts recreate their databases, so do not run them again if you want to keep existing data.

### 2. Check the Lab 2 Database

Our website also uses the `registration` database from Lab 2, which contains the `users` and `todos` tables.

If it already exists, keep it as it is.

If it does not exist, create it using `website/database/schema.sql`. Do not rerun this script on a database containing data you want to keep.

### 3. Configure the Website

Open the `website` folder in VS Code.

Copy `.env.example` to a new file named `.env` and set your local MySQL connection details.

Use:

- `DB_NAME=registration`
- `LIBRARY_DB_NAME=library`

Also set your MySQL password and a Flask `SECRET_KEY`.

### 4. Install the Requirements

Open the VS Code terminal inside the `website` folder and run:

```powershell
python -m pip install -r requirements.txt
```

### 5. Run Flask

In the same terminal, run:

```powershell
python app.py
```

Then open:

`http://127.0.0.1:5000`

### 6. Test the Website

- Register a new account or log in with an existing one.
- Open the To-Do List and test the tasks.
- Open Library to see the authors and books.
- Try adding and editing an author or book.
- Upload an author photo or a book cover.
- Try deleting a test record.
- Log out when finished.

## Project Files

```text
lab3/
├── problem1_DDL.sql
├── problem1_DML.sql
├── problem1_Answers.txt
├── problem2_DDL.sql
├── problem2_DML.sql
├── README.md
└── website/
    ├── app.py
    ├── requirements.txt
    ├── .env.example
    ├── .gitignore
    ├── database/
    ├── templates/
    └── static/
        ├── style.css
        ├── app.js
        └── uploads/
            ├── authors/
            └── books/
```

## Notes

- We used simple SQL queries for adding, editing, deleting, and displaying data.
- The Library database uses a foreign key to connect books with authors.
- The website requires both the `registration` and `library` databases.
- Do not upload the `.env` file or database passwords to GitHub.
- The bonus images are saved as files, not as binary data inside MySQL.
- On another computer, uploaded images will only display if the image files and matching database records are both available.