CREATE DATABASE IF NOT EXISTS blog_db;
USE blog_db;

CREATE TABLE IF NOT EXISTS posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    content TEXT,
    INDEX ix_posts_id (id),
    INDEX ix_posts_title (title)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;