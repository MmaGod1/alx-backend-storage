-- Creates a users table with
-- id, email and name fields
CREATE TABLE if NOT EXISTS users (
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255)
)
