CREATE SCHEMA IF NOT EXISTS `Koppe2` DEFAULT CHARACTER SET utf8 ;
USE `Koppe2` ;

-- -----------------------------------------------------
-- Table `Koppe2`.`Registro`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Koppe2`.`Registro` (
  `ID_Registro` INT NOT NULL AUTO_INCREMENT,
  `Nombre_Cliente` VARCHAR(45) NOT NULL,
  `Email_Cliente` VARCHAR(45) NOT NULL,
  `Contraseña_Usuario` VARCHAR(150) NOT NULL,
  `Rol_Usuario` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`ID_Registro`))
ENGINE = InnoDB;

/* En esta parte arpovecho y le digo a SQl que el rol usuario por default va a 
ser 'cliente' y así aunque el usuario no eliga el rol tendra uno por defecto 
que es el de usuario. PDT: El problema es para cuando se quiera registrar a 
otro usuario como administrador. */

ALTER TABLE `koppe2`.`registro` 
CHANGE COLUMN `Rol_Usuario` `Rol_Usuario` VARCHAR(45) NOT NULL DEFAULT 'cliente' ;

-- -----------------------------------------------------
-- Table `Koppe2`.`Reservas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Koppe2`.`Reservas` (
  `ID_Reserva` INT NOT NULL AUTO_INCREMENT,
  `Cantidad_De_Sillas` INT NOT NULL,
  `Hora_Reserva` TIME NOT NULL,
  `Fecha_Reserva` DATE NOT NULL,
  `Cliente_ID_F` INT NOT NULL,
  PRIMARY KEY (`ID_Reserva`))
ENGINE = InnoDB;

/* Acá se crea la llave foranea de la tabla de reservas, la cual conecta
Cliente_ID_F (Cliente_ID_Foraneo) y ID_Registro (Que es el ID del usuario en
la tabla original) */

ALTER TABLE `koppe2`.`reservas` 
ADD INDEX `ID_Persona_Reserva_idx` (`Cliente_ID_F` ASC);
;
ALTER TABLE `koppe2`.`reservas` 
ADD CONSTRAINT `ID_Persona_Reserva`
  FOREIGN KEY (`Cliente_ID_F`)
  REFERENCES `koppe2`.`registro` (`ID_Registro`)
  ON DELETE CASCADE
  ON UPDATE CASCADE;
  
update Registro set Rol_Usuario = "administrador" where ID_Registro = 1;
select * from Registro;
select * from Reservas;
select * from Comentarios;


SELECT Fecha_Reserva FROM Reservas WHERE Cliente_ID_F = 3 ORDER BY Fecha_Reserva DESC LIMIT 1;

SELECT Reservas.ID_Reserva, Registro.Nombre_Cliente, Registro.Email_Cliente, Reservas.Cantidad_De_Sillas, Reservas.Hora_Reserva, Reservas.Fecha_Reserva FROM Registro INNER JOIN Reservas ON ID_Registro = Cliente_ID_F;

  CREATE TABLE Comentarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    texto text(200) NOT NULL,
    usuario_id INT NOT NULL,
    calificacion INT NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES Registro(ID_Registro)
  );

ALTER TABLE `koppe2`.`comentarios` 
DROP FOREIGN KEY `comentarios_ibfk_1`;
ALTER TABLE `koppe2`.`comentarios` 
ADD CONSTRAINT `comentarios_id_Registro`
  FOREIGN KEY (`usuario_id`)
  REFERENCES `koppe2`.`registro` (`ID_Registro`)
  ON DELETE CASCADE
  ON UPDATE CASCADE;
  



