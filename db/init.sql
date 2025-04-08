-- Create healthcheck user
CREATE USER IF NOT EXISTS 'healthcheck'@'localhost' IDENTIFIED BY '${MYSQL_PASSWORD}';
GRANT USAGE ON *.* TO 'healthcheck'@'localhost';

-- Create application database and user
CREATE DATABASE IF NOT EXISTS todo CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE todo;

-- Create todos table and indexes first
CREATE TABLE IF NOT EXISTS todos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create indexes
CREATE INDEX idx_completed ON todos(completed);
CREATE INDEX idx_created_at ON todos(created_at);

-- Create application user
CREATE USER IF NOT EXISTS 'todo'@'%' IDENTIFIED BY 'todo_password';
GRANT ALL PRIVILEGES ON todo.* TO 'todo'@'%';

FLUSH PRIVILEGES; 