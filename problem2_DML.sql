USE library;

INSERT IGNORE INTO AUTHOR (author_id, name, country) VALUES
(1, 'Dodo', 'Egypt'),
(2, 'Mohamed Bory', 'Egypt'),
(3, 'Eng Basem', 'Egypt');

INSERT IGNORE INTO BOOK (book_id, title, price, author_id) VALUES
(1, 'Palace Walk', 250, 1),
(2, 'Palace of Desire', 280, 1),
(3, 'Murder on the Orient Express', 320, 2),
(4, 'And Then There Were None', 300, 2),
(5, 'Animal Farm', 400, 3),
(6, '1984', 500, 3);

SELECT * FROM AUTHOR;
SELECT * FROM BOOK;