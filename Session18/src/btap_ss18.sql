DROP DATABASE IF EXISTS btap_ss18;

CREATE DATABASE btap_ss18;

USE btap_ss18;


-- =========================
-- STUDENTS
-- =========================

CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE'
);


-- =========================
-- COURSES
-- =========================

CREATE TABLE courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    max_students INT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'OPEN'
);


-- =========================
-- ENROLLMENTS
-- =========================

CREATE TABLE enrollments (
    id INT AUTO_INCREMENT PRIMARY KEY,

    student_id INT NOT NULL,
    course_id INT NOT NULL,

    enrolled_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    status VARCHAR(20) NOT NULL DEFAULT 'STUDYING',

    FOREIGN KEY (student_id)
        REFERENCES students(id),

    FOREIGN KEY (course_id)
        REFERENCES courses(id),

    UNIQUE (student_id, course_id)
);


-- =========================
-- STUDENTS DATA
-- =========================

INSERT INTO students (full_name, email, status)
VALUES
('Nguyễn Văn An', 'an@gmail.com', 'ACTIVE'),
('Trần Văn Bình', 'binh@gmail.com', 'ACTIVE'),
('Lê Văn Cường', 'cuong@gmail.com', 'INACTIVE'),
('Phạm Thị Dung', 'dung@gmail.com', 'ACTIVE');


-- =========================
-- COURSES DATA
-- =========================

INSERT INTO courses (name, max_students, status)
VALUES
('FastAPI Basic', 30, 'OPEN'),
('Python Advanced', 2, 'OPEN'),
('SQLAlchemy ORM', 20, 'OPEN'),
('Java Spring Boot', 30, 'CLOSED');


-- =========================
-- ENROLLMENTS DATA
-- =========================

INSERT INTO enrollments
    (student_id, course_id, status)
VALUES
    (1, 1, 'STUDYING'),
    (1, 2, 'STUDYING'),
    (2, 1, 'STUDYING');