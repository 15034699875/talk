CREATE DATABASE IF NOT EXISTS talk DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE talk;

CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) UNIQUE,
  password_hash CHAR(60),
  avatar_url VARCHAR(255),
  points INT DEFAULT 0,
  exp BIGINT DEFAULT 0,
  role ENUM('user','admin') DEFAULT 'user',
  email VARCHAR(120) UNIQUE,
  is_banned BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS groups (
  id INT AUTO_INCREMENT PRIMARY KEY,
  owner_id INT,
  name VARCHAR(100),
  FOREIGN KEY (owner_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS group_members (
  user_id INT,
  group_id INT,
  role ENUM('owner','admin','member'),
  PRIMARY KEY (user_id, group_id),
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (group_id) REFERENCES groups(id)
);

CREATE TABLE IF NOT EXISTS point_logs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT,
  change INT NOT NULL,
  reason VARCHAR(100),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
); 