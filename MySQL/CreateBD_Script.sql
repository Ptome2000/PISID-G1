-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema marsami_game
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema marsami_game
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `marsami_game` DEFAULT CHARACTER SET utf8 ;
USE `marsami_game` ;

-- -----------------------------------------------------
-- Table `marsami_game`.`User`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `marsami_game`.`User` (
  `IDUser` INT NOT NULL AUTO_INCREMENT,
  `Nome` VARCHAR(100) NULL,
  `Telemovel` DECIMAL(12) NULL,
  `Tipo` VARCHAR(3) NOT NULL,
  `Email` VARCHAR(50) NOT NULL,
  `Password` VARCHAR(45) NOT NULL,
  `Grupo` INT NULL,
  `Username` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`IDUser`),
  UNIQUE INDEX `Cellphone_UNIQUE` (`Telemovel` ASC),
  UNIQUE INDEX `Email_UNIQUE` (`Email` ASC),
  UNIQUE INDEX `UserID_UNIQUE` (`IDUser` ASC),
  UNIQUE INDEX `Username_UNIQUE` (`Username` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `marsami_game`.`Game`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `marsami_game`.`Game` (
  `IDJogo` INT NOT NULL AUTO_INCREMENT,
  `StartDate` DATETIME NOT NULL,
  `GameOver` TINYINT NOT NULL,
  `UserID` INT NOT NULL,
  `Description` VARCHAR(200) NULL,
  `GameName` VARCHAR(50) NULL,
  `TotalMarsamis` INT NOT NULL,
  `SoundVarTolerance` DOUBLE NOT NULL,
  `BaseSound` DOUBLE NOT NULL,
  PRIMARY KEY (`IDJogo`),
  UNIQUE INDEX `StartDate_UNIQUE` (`StartDate` ASC),
  INDEX `fk_Game_User1_idx` (`UserID` ASC),
  CONSTRAINT `fk_Game_User1`
    FOREIGN KEY (`UserID`)
    REFERENCES `marsami_game`.`User` (`IDUser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `marsami_game`.`Marsami`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `marsami_game`.`Marsami` (
  `IDMarsami` INT NOT NULL AUTO_INCREMENT,
  `MarsamiNumber` INT NOT NULL,
  `CurrStatus` ENUM('0', '1', '2') NOT NULL,
  `CurrRoom` INT NOT NULL,
  `GameID` INT NOT NULL,
  PRIMARY KEY (`IDMarsami`),
  INDEX `fk_Marsami_Game1_idx` (`GameID` ASC),
  CONSTRAINT `fk_Marsami_Game1`
    FOREIGN KEY (`GameID`)
    REFERENCES `marsami_game`.`Game` (`IDJogo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `marsami_game`.`Movement`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `marsami_game`.`Movement` (
  `IDMovement` INT NOT NULL AUTO_INCREMENT,
  `OriginRoom` INT NOT NULL,
  `DestinationRoom` INT NOT NULL,
  `Status` ENUM('0', '1', '2') NOT NULL,
  `Hour` DATETIME NOT NULL,
  `MarsamiID` INT NOT NULL,
  `IDGame` INT NOT NULL,
  INDEX `fk_Movement_Marsami1_idx` (`MarsamiID` ASC),
  PRIMARY KEY (`IDMovement`),
  INDEX `fk_Movement_Game1_idx` (`IDGame` ASC),
  CONSTRAINT `fk_Movement_Marsami1`
    FOREIGN KEY (`MarsamiID`)
    REFERENCES `marsami_game`.`Marsami` (`IDMarsami`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Movement_Game1`
    FOREIGN KEY (`IDGame`)
    REFERENCES `marsami_game`.`Game` (`IDJogo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `marsami_game`.`Sound`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `marsami_game`.`Sound` (
  `IDSound` INT NOT NULL AUTO_INCREMENT,
  `Sound` VARCHAR(12) NOT NULL,
  `Hour` DATETIME NOT NULL,
  `IDGame` INT NOT NULL,
  PRIMARY KEY (`IDSound`),
  INDEX `fk_Sound_Game1_idx` (`IDGame` ASC),
  CONSTRAINT `fk_Sound_Game1`
    FOREIGN KEY (`IDGame`)
    REFERENCES `marsami_game`.`Game` (`IDJogo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `marsami_game`.`Message`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `marsami_game`.`Message` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Hora` DATETIME NULL,
  `Sala` INT NULL,
  `GameID` INT NOT NULL,
  `Sensor` INT NULL,
  `Leitura` DECIMAL(6,2) NULL,
  `TipoAlerta` VARCHAR(50) NULL,
  `Msg` VARCHAR(100) NULL,
  `HoraEscrita` DATETIME NULL,
  PRIMARY KEY (`ID`),
  INDEX `fk_Message_Game1_idx` (`GameID` ASC),
  CONSTRAINT `fk_Message_Game1`
    FOREIGN KEY (`GameID`)
    REFERENCES `marsami_game`.`Game` (`IDJogo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `marsami_game`.`Corridor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `marsami_game`.`Corridor` (
  `IDCorridor` INT NOT NULL,
  `OriginRoom` INT NOT NULL,
  `DestinationRoom` INT NOT NULL,
  `Distance` INT NOT NULL,
  `isClosed` TINYINT NOT NULL,
  `GameID` INT NOT NULL,
  PRIMARY KEY (`IDCorridor`),
  INDEX `FKGame` (`GameID` ASC),
  UNIQUE INDEX `uniqueRoomComb` (`DestinationRoom` ASC, `OriginRoom` ASC),
  CONSTRAINT `fk_Corridor_Game1`
    FOREIGN KEY (`GameID`)
    REFERENCES `marsami_game`.`Game` (`IDJogo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `marsami_game`.`Occupation`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `marsami_game`.`Occupation` (
  `IDJogo` INT NOT NULL,
  `NumeroMarsamisOdd` INT NOT NULL,
  `NumeroMarsamisEven` INT NOT NULL,
  `Sala` INT NOT NULL,
  INDEX `fk_Occupation_Game1_idx` (`IDJogo` ASC),
  PRIMARY KEY (`IDJogo`),
  CONSTRAINT `fk_Occupation_Game1`
    FOREIGN KEY (`IDJogo`)
    REFERENCES `marsami_game`.`Game` (`IDJogo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
