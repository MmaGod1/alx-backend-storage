-- Creates a users table with
-- id, email, name, country(enumeration of countries: US, CO and TN) fields
CREATE TABLE if NOT EXISTS users (
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255),
    country ENUM('US', 'CO', 'TN') DEFAULT 'US' NOT NULL
)
