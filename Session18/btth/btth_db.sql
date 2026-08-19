CREATE DATABASE btth_ss18;
USE btth_ss18;


-- =========================
-- DEPARTMENTS
-- =========================

CREATE TABLE departments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);


-- =========================
-- STUDENTS
-- =========================

CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    department_id INT NOT NULL,

    FOREIGN KEY (department_id)
        REFERENCES departments(id)
);


-- =========================
-- COURSES
-- =========================

CREATE TABLE courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'OPEN'
);


-- =========================
-- ENROLLMENTS
-- =========================

CREATE TABLE enrollments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,

    FOREIGN KEY (student_id)
        REFERENCES students(id),

    FOREIGN KEY (course_id)
        REFERENCES courses(id),

    UNIQUE (student_id, course_id)
);


-- =========================
-- DEPARTMENTS DATA
-- =========================

INSERT INTO departments (name)
VALUES
('Công nghệ thông tin'),
('Kinh tế');


-- =========================
-- STUDENTS DATA
-- =========================

INSERT INTO students (
    full_name,
    status,
    department_id
)
VALUES
('Nguyễn Văn An', 'ACTIVE', 1),
('Trần Văn Bình', 'INACTIVE', 1),
('Lê Thị Dung', 'ACTIVE', 2);


-- =========================
-- COURSES DATA
-- =========================

INSERT INTO courses (name, status)
VALUES
('FastAPI Basic', 'OPEN'),
('Python Advanced', 'OPEN'),
('Java Spring Boot', 'CLOSED');


-- =========================
-- ENROLLMENTS DATA
-- =========================

INSERT INTO enrollments (
    student_id,
    course_id
)
VALUES
(1, 1);