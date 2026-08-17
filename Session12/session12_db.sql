CREATE DATABASE IF NOT EXISTS session12_db;
USE session12_db;

CREATE TABLE shipments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tracking_code VARCHAR(50) NOT NULL UNIQUE,
    receiver_name VARCHAR(100) NOT NULL,
    delivery_address VARCHAR(255) NOT NULL
);

CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE documents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    subject VARCHAR(100) NOT NULL,
    document_type VARCHAR(100) NOT NULL,
    file_url VARCHAR(500) NOT NULL
);

INSERT INTO documents (title, subject, document_type, file_url)
VALUES
(
    'Giáo trình Python cơ bản',
    'Python',
    'PDF',
    'https://example.com/python-basic.pdf'
),
(
    'Slide SQLAlchemy ORM',
    'FastAPI',
    'Slide',
    'https://example.com/sqlalchemy-slide.pdf'
),
(
    'Đề thi cuối kỳ',
    'Cơ sở dữ liệu',
    'Exam',
    'https://example.com/database-exam.pdf'
);

INSERT INTO shipments (tracking_code, receiver_name, delivery_address)
VALUES
('GH001', 'Nguyen Van A', 'Ha Noi'),
('GH002', 'Tran Thi B', 'Hai Phong'),
('GH003', 'Le Van C', 'Da Nang');

INSERT INTO students(full_name,email)
VALUES
("Nguyen Van A","vana@gmail.com"),
("Tran Thi B","tran@gmail.com"),
("Le Van C","levan@gmail.com");

