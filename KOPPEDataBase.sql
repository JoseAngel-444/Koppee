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


