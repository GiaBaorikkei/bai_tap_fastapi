CREATE DATABASE IF NOT EXISTS course_management;

USE course_management;

CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    status VARCHAR(20) DEFAULT 'ACTIVE'
);


CREATE TABLE courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    max_students INT NOT NULL
);


CREATE TABLE enrollments (
    id INT AUTO_INCREMENT PRIMARY KEY,

    student_id INT NOT NULL,
    course_id INT NOT NULL,

    enrolled_at DATETIME DEFAULT CURRENT_TIMESTAMP,

	FOREIGN KEY (student_id)
	REFERENCES students(id),
	FOREIGN KEY (course_id)
	REFERENCES courses(id)
);

INSERT INTO students (full_name, status)
VALUES
('Nguyễn Văn An', 'ACTIVE'),
('Trần Văn Bình', 'ACTIVE'),
('Lê Thị Hoa', 'ACTIVE');


INSERT INTO courses (name, max_students)
VALUES
('FastAPI Basic', 30),
('Python Basic', 40),
('SQLAlchemy ORM', 25);

INSERT INTO enrollments (student_id, course_id)
VALUES
(1, 1),
(1, 2),
(2, 1),
(3, 3);