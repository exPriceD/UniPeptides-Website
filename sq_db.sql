CREATE TABLE IF NOT EXISTS users (
id integer PRIMARY KEY AUTOINCREMENT,
username text NOT NULL,
email text NOT NULL,
password text NOT NULL
);

CREATE TABLE IF NOT EXISTS searchResults (
id integer PRIMARY KEY AUTOINCREMENT,
username text NOT NULL,
email text NOT NULL,
tm text NOT NULL,
file BLOB NOT NULL,
peptides text NOT NULL,
proteins text NOT NULL
);

CREATE TABLE IF NOT EXISTS databaseResults (
id integer PRIMARY KEY AUTOINCREMENT,
username text NOT NULL,
email text NOT NULL,
tm text NOT NULL,
file BLOB NOT NULL,
peptides text NOT NULL
);