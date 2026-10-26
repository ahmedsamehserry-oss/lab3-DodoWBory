# Database Lab 3 — Flask Library + Lab 2 To-Do

## Features

- Retains Lab 2 registration, login, session protection and user-specific to-do CRUD.
- Registration now sends the user to Login; successful Login opens My Tasks.
- A **Library** navigation link opens `/library` after login.
- Shows **AUTHOR** and **BOOK** tables (including `author_id` on each book).
- Add, edit and delete authors and books using separate parameterized SQL statements (no JOIN needed).
- Deleting an author removes their books automatically via `ON DELETE CASCADE` in MySQL.
- **BONUS:** upload or replace author photos and book cover images via the website; display saved images in both tables.
- Maximum image size 3 MB; accepts PNG/JPG/WEBP/GIF, re-encodes uploaded images to WEBP and generates random filenames.
- CSRF tokens in forms, logged-in-only mutation routes, server-side input validation, mobile-responsive UI.

## Folder / database requirements

This `website/` is adapted from the available Lab 2 archive; it is a full website folder, not a SQL script. It needs BOTH existing MySQL databases:

- `registration` — from Lab 2 (`database/schema.sql`). It holds `users` and `todos`.
- `library` — created with the separate `problem2_DDL.sql` file for Lab 3. It holds `AUTHOR` and `BOOK`.

IMPORTANT: **Do not run** `website/database/schema.sql` if you want to preserve existing Lab 2 users/tasks. Do not rerun `problem2_DDL.sql` after adding library data, because it drops the `library` database.

## Windows setup (before demonstration)

1. Start MySQL Server. In Workbench verify:
   ```sql
   USE registration;
   SELECT COUNT(*) FROM users;
   USE library;
   SELECT COUNT(*) FROM AUTHOR;
   SELECT COUNT(*) FROM BOOK;
   ```
   Lab 3 seed data should include at least 3 authors and 6 books.
2. Extract this ZIP, and place `website` inside your existing `Lab 3` folder.
3. If you already have a working Lab 2 `.env`, **copy** it into the new `website` folder. Otherwise, copy `.env.example` to `.env` and supply your MySQL password + unique `SECRET_KEY`. Keep `DB_NAME=registration` and add `LIBRARY_DB_NAME=library`.
4. Open the new `website` folder in VS Code and open its terminal.
5. Install dependencies (once):
   ```powershell
   python -m pip install -r requirements.txt
   ```
   If `python` fails, use `py` instead.
6. Run the app:
   ```powershell
   python app.py
   ```
7. Open **http://127.0.0.1:5000**. Register → Login → My Tasks. Click **Library** for books/authors. Upload a book cover or author photo with the add/edit forms. The bonus is not illustrated until you upload real images.

Uploaded pictures are stored in `static/uploads/authors` and `static/uploads/books` and their file names in `library.AUTHOR.photo_filename` and `library.BOOK.cover_filename`. They are not stored as binary BLOBs in MySQL.

## What to submit

Place `website/` alongside these files in the Lab 3 folder:

- `problem1_DDL.sql`
- `problem1_DML.sql` (YOUR actual edited sample data)
- `problem1_Answers.txt` (YOUR actual SQL output/error text)
- `problem2_DDL.sql`
- `problem2_DML.sql` (YOUR actual authors/books seed data)
- `README.md` at Lab 3 root (include both databases' setup and web steps)

All students should obey the handout's individual-work policy. Never upload `.env` or actual passwords. To demonstrate seeded photos on another machine, keep the images in the appropriate `static/uploads/` subfolders and set matching file names in its database; otherwise demonstrate the bonus by uploading through the UI.

## Demonstration checklist

- Registration -> Login -> My Tasks; add, edit, done/undo, delete; see counters
- Library shows 3+ authors and 6+ books, including each book's `author_id`
- Add and edit an author, optionally add a photo
- Add and edit a book, optionally add a cover
- Delete a book; delete an author -> confirm associated books vanish (`ON DELETE CASCADE`)
- Logout -> Login
