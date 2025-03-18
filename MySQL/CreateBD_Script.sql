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
-- Table `marsami_game`.`Configuration`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `marsami_game`.`Configuration` (
  `ConfigID` INT NOT NULL AUTO_INCREMENT,
  `TotalMarsamis` INT NOT NULL,
  `SoundLimit` DOUBLE NOT NULL,
  `MarsamisTTL` INT NOT NULL,
  PRIMARY KEY (`ConfigID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `marsami_game`.`User`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `marsami_game`.`User` (
  `UserID` INT NOT NULL,
  `Name` VARCHAR(45) NULL,
  `Cellphone` DECIMAL(9) NULL,
  `Type` ENUM('Admin', 'Player') NOT NULL,
  `Email` VARCHAR(45) NOT NULL,
  `Password` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`UserID`),
  UNIQUE INDEX `Cellphone_UNIQUE` (`Cellphone` ASC),
  UNIQUE INDEX `Email_UNIQUE` (`Email` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `marsami_game`.`Game`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `marsami_game`.`Game` (
  `GameID` INT NOT NULL AUTO_INCREMENT,
  `PlayerID` INT NOT NULL,
  `StartDate` DATETIME NOT NULL,
  `GameOver` TINYINT NOT NULL,
  `ConfigID` INT NOT NULL,
  `UserID` INT NOT NULL,
  PRIMARY KEY (`GameID`),
  UNIQUE INDEX `StartDate_UNIQUE` (`StartDate` ASC),
  INDEX `fk_Game_Configuration1_idx` (`ConfigID` ASC),
  INDEX `fk_Game_User1_idx` (`UserID` ASC),
  CONSTRAINT `fk_Game_Configuration1`
    FOREIGN KEY (`ConfigID`)
    REFERENCES `marsami_game`.`Configuration` (`ConfigID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Game_User1`
    FOREIGN KEY (`UserID`)
    REFERENCES `marsami_game`.`User` (`UserID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `marsami_game`.`Message`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `marsami_game`.`Message` (
  `MessageID` INT NOT NULL AUTO_INCREMENT,
  `RegisteredDate` DATETIME NOT NULL,
  `Type` ENUM('Move', 'Sound') NULL,
  `GameID` INT NOT NULL,
  PRIMARY KEY (`MessageID`),
  INDEX `fk_Message_Game1_idx` (`GameID` ASC),
  CONSTRAINT `fk_Message_Game1`
    FOREIGN KEY (`GameID`)
    REFERENCES `marsami_game`.`Game` (`GameID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `marsami_game`.`Marsami`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `marsami_game`.`Marsami` (
  `MarsamiID` INT NOT NULL AUTO_INCREMENT,
  `MarsamiNumber` INT NOT NULL,
  `CurrStatus` ENUM('0', '1', '2') NOT NULL,
  `CurrRoom` INT NOT NULL,
  `GameID` INT NOT NULL,
  PRIMARY KEY (`MarsamiID`),
  INDEX `fk_Marsami_Game1_idx` (`GameID` ASC),
  CONSTRAINT `fk_Marsami_Game1`
    FOREIGN KEY (`GameID`)
    REFERENCES `marsami_game`.`Game` (`GameID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `marsami_game`.`Movement`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `marsami_game`.`Movement` (
  `OriginRoom` INT NOT NULL,
  `DestinationRoom` INT NOT NULL,
  `Status` ENUM('0', '1', '2') NOT NULL,
  `MessageID` INT NOT NULL,
  `MarsamiID` INT NOT NULL,
  PRIMARY KEY (`MessageID`),
  INDEX `fk_Movement_Message1_idx` (`MessageID` ASC),
  INDEX `fk_Movement_Marsami1_idx` (`MarsamiID` ASC),
  CONSTRAINT `fk_Movement_Message1`
    FOREIGN KEY (`MessageID`)
    REFERENCES `marsami_game`.`Message` (`MessageID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Movement_Marsami1`
    FOREIGN KEY (`MarsamiID`)
    REFERENCES `marsami_game`.`Marsami` (`MarsamiID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `marsami_game`.`Sound`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `marsami_game`.`Sound` (
  `Sound` DOUBLE NOT NULL,
  `MessageID` INT NOT NULL,
  PRIMARY KEY (`MessageID`),
  INDEX `fk_Sound_Message_idx` (`MessageID` ASC),
  CONSTRAINT `fk_Sound_Message`
    FOREIGN KEY (`MessageID`)
    REFERENCES `marsami_game`.`Message` (`MessageID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `marsami_game`.`Corridor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `marsami_game`.`Corridor` (
  `CorridorID` INT NOT NULL,
  `OriginRoom` INT NOT NULL,
  `DestinationRoom` INT NOT NULL,
  `Distance` INT NOT NULL,
  `isClosed` TINYINT NOT NULL,
  `GameID` INT NOT NULL,
  PRIMARY KEY (`CorridorID`),
  INDEX `FKGame` (`GameID` ASC),
  UNIQUE INDEX `uniqueRoomComb` (`DestinationRoom` ASC, `OriginRoom` ASC),
  CONSTRAINT `fk_Corridor_Game1`
    FOREIGN KEY (`GameID`)
    REFERENCES `marsami_game`.`Game` (`GameID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `marsami_game`.`Occupation`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `marsami_game`.`Occupation` (
  `OccupationID` INT NOT NULL,
  `MarsamisOdd` INT NULL,
  `MarsamisEven` INT NULL,
  `RoomNumber` INT NULL,
  `GameID` INT NOT NULL,
  PRIMARY KEY (`OccupationID`),
  INDEX `fk_Occupation_Game1_idx` (`GameID` ASC),
  CONSTRAINT `fk_Occupation_Game1`
    FOREIGN KEY (`GameID`)
    REFERENCES `marsami_game`.`Game` (`GameID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
