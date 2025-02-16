sudo mysql_secure_installation

sudo mysql -u root

CREATE USER 'mysql'@'172.31.0.%' IDENTIFIED BY 'admin123!!!';
GRANT ALL PRIVILEGES ON *.* TO 'mysql'@'172.31.0.%' WITH GRANT OPTION;
FLUSH PRIVILEGES;

CREATE USER 'api_user'@'%' IDENTIFIED BY 'strongpassword';
GRANT SELECT ON *.* TO 'api_user'@'%';
FLUSH PRIVILEGES;

SELECT user, host FROM mysql.user;

SHOW GRANTS FOR 'mysql'@'172.31.0.%';
SHOW GRANTS FOR 'api_user'@'%';

CREATE DATABASE dummy_db;

USE dummy_db;

CREATE TABLE employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hire_date DATE NOT NULL
);

INSERT INTO employees (first_name, last_name, email, hire_date) VALUES
('John', 'Doe', 'john.doe@example.com', '2020-01-15'),
('Jane', 'Smith', 'jane.smith@example.com', '2019-07-22'),
('Alice', 'Johnson', 'alice.johnson@example.com', '2021-03-05'),
('Bob', 'Williams', 'bob.williams@example.com', '2018-11-30'),
('Eve', 'Davis', 'eve.davis@example.com', '2022-06-10');

SELECT * FROM employees;
