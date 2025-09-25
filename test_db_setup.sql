CREATE USER 'test'@'localhost' IDENTIFIED WITH caching_sha2_password BY 'test';
GRANT ALL PRIVILEGES ON test.* TO 'test'@'localhost';
FLUSH ALL PRIVILEGES;
CREATE DATABASE test;