CREATE DATABASE hobbies;
use hobbies;

CREATE TABLE user(
   id int primary key auto_increment,
   name_user varchar(60) NOT NULL,
   email_user varchar(60) NOT NULL,
   password_user char(8) NOT NULL    
);

CREATE TABLE hobby (
   id INT PRIMARY KEY AUTO_INCREMENT,         
   tipo VARCHAR(50) NOT NULL,   
   nome VARCHAR(50) NOT NULL,     
   usuario_id INT,                  
   FOREIGN KEY (usuario_id) REFERENCES user(id)  
);

select * from user;