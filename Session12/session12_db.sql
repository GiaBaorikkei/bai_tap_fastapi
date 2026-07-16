CREATE DATABASE IF NOT EXISTS session12_db;
USE session12_db;

CREATE TABLE shipments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tracking_code VARCHAR(50) NOT NULL UNIQUE,
    receiver_name VARCHAR(100) NOT NULL,
    delivery_address VARCHAR(255) NOT NULL
);

INSERT INTO shipments (tracking_code, receiver_name, delivery_address)
VALUES
('1', 'Nguyen Van A', 'Ha Noi'),
('2', 'Tran Thi B', 'Hai Phong'),
('3', 'Le Van C', 'Da Nang');

