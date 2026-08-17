CREATE DATABASE IF NOT EXISTS fastapi;
USE fastapi;
-- TẠO 2 BẢNG DỮ LIỆU: CLASSROOMS VÀ STUDENT
create table classrooms (
	id int primary key auto_increment,
    class_name varchar(100) not null
);

create table students (
	id int primary key auto_increment,
    name varchar(50) not null,
    email varchar(100) not null unique,
    class_id int,
    foreign key (class_id) references classrooms(id)
);	