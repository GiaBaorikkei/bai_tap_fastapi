CREATE DATABASE IF NOT EXISTS connect_db;
USE connect_db;

-- Bảng Products
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    price DECIMAL(12,2) NOT NULL
);

-- Bảng Students
CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    class_name VARCHAR(20) NOT NULL,
    email VARCHAR(50) NOT NULL
);

-- Bảng Shipments
CREATE TABLE shipments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tracking_number VARCHAR(50) NOT NULL UNIQUE,
    status VARCHAR(50) NOT NULL DEFAULT 'PREPARING'
);

-- Bảng Customers
CREATE TABLE customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Bảng Memberships
CREATE TABLE memberships (
    id INT AUTO_INCREMENT PRIMARY KEY,
    card_number VARCHAR(50) NOT NULL UNIQUE,
    customer_id INT NOT NULL,
    FOREIGN KEY (customer_id)
        REFERENCES customers(id)
);

-- Bảng Parking Slots
CREATE TABLE parking_slots (
    id INT AUTO_INCREMENT PRIMARY KEY,
    slot_code VARCHAR(50) NOT NULL UNIQUE,
    zone_name VARCHAR(255) NOT NULL,
    max_weight INT NOT NULL,
    is_available BOOLEAN NOT NULL DEFAULT TRUE
);

