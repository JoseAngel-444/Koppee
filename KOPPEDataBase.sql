create database koppe2;
use koppa2;
create table registro(
docid varchar(50)not null, id int(10) primary key not null, 
nombrecli varchar(50) not null,
apellidocli varchar(50) not null, email varchar(50) not null, 
usuariocli varchar(50), contracli varchar(225) not null,
rol ENUM('cliente', 'administrador') NOT NULL);
create table reservas(
codmesa int primary key not null, numerosillas int not null, 
fechareserva date not null, horarioreserva time not null);
describe registro;
show tables;
select * from registro;