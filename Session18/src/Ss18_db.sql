create database session18;
use session18;

create table category(
	id int primary key auto_increment,
    name varchar(100) not null unique
);

create table product(
	id int primary key auto_increment,
    product_name varchar(100) not null,
    price decimal(12,2) check(price>=0),
    category_id int,
    foreign key (category_id) references category(id)
);