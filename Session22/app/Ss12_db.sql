CREATE DATABASE IF NOT EXISTS Ss22_db;
USE Ss22_db;

create table users (
	 id int primary key auto_increment,
     username varchar(100) not null unique,
     password varchar(50) not null
);