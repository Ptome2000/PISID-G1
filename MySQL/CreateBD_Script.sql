-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.4.32-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             12.10.0.7000
-- --------------------------------------------------------
/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;

/*!40101 SET NAMES utf8 */;

/*!50503 SET NAMES utf8mb4 */;

/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;

/*!40103 SET TIME_ZONE='+00:00' */;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;

/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Dumping database structure for marsami_game
DROP DATABASE IF EXISTS `marsami_game`;

CREATE DATABASE IF NOT EXISTS `marsami_game` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci */;

USE `marsami_game`;

-- Dumping structure for table marsami_game.game
CREATE TABLE IF NOT EXISTS `game` (
  `IDJogo` int(11) NOT NULL AUTO_INCREMENT,
  `StartDate` datetime DEFAULT CURRENT_TIMESTAMP,
  `GameOver` tinyint (4) NOT NULL,
  `Description` varchar(200) DEFAULT NULL,
  `Username` varchar(50) DEFAULT NULL,
  `GameName` varchar(50) DEFAULT NULL,
  `TotalMarsamis` int(11) NOT NULL,
  `SoundVarTolerance` double NOT NULL,
  `BaseSound` double NOT NULL,
  `TotalRooms` int(11) NOT NULL,
  PRIMARY KEY (`IDJogo`),
  UNIQUE KEY `StartDate_UNIQUE` (`StartDate`),
  KEY `FK_game_user` (`Username`),
  CONSTRAINT `FK_game_user` FOREIGN KEY (`Username`) REFERENCES `user` (`Username`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8 COLLATE = utf8_general_ci;

-- Data exporting was unselected.
-- Dumping structure for table marsami_game.marsami
CREATE TABLE IF NOT EXISTS `marsami` (
  `IDMarsami` int(11) NOT NULL AUTO_INCREMENT,
  `MarsamiNumber` int(11) NOT NULL,
  `CurrStatus` enum ('0', '1', '2') NOT NULL,
  `CurrRoom` int(11) NOT NULL,
  `GameID` int(11) NOT NULL,
  PRIMARY KEY (`IDMarsami`),
  KEY `fk_Marsami_Game1_idx` (`GameID`),
  CONSTRAINT `fk_Marsami_Game1` FOREIGN KEY (`GameID`) REFERENCES `game` (`IDJogo`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB DEFAULT CHARSET = utf8 COLLATE = utf8_general_ci;

-- Data exporting was unselected.
-- Dumping structure for table marsami_game.message
CREATE TABLE IF NOT EXISTS `message` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Hora` datetime DEFAULT NULL,
  `Sala` int(11) DEFAULT NULL,
  `GameID` int(11) NOT NULL,
  `Sensor` int(11) DEFAULT NULL,
  `Leitura` decimal(6, 2) DEFAULT NULL,
  `TipoAlerta` varchar(50) DEFAULT NULL,
  `Msg` varchar(100) DEFAULT NULL,
  `HoraEscrita` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`),
  KEY `fk_Message_Game1_idx` (`GameID`),
  CONSTRAINT `fk_Message_Game1` FOREIGN KEY (`GameID`) REFERENCES `game` (`IDJogo`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB DEFAULT CHARSET = utf8 COLLATE = utf8_general_ci;

-- Data exporting was unselected.
-- Dumping structure for table marsami_game.movement
CREATE TABLE IF NOT EXISTS `movement` (
  `IDMovement` int(11) NOT NULL AUTO_INCREMENT,
  `OriginRoom` int(11) NOT NULL,
  `DestinationRoom` int(11) NOT NULL,
  `Status` enum ('0', '1', '2') NOT NULL,
  `Hour` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `MarsamiNum` int(11) NOT NULL,
  `IDGame` int(11) NOT NULL,
  PRIMARY KEY (`IDMovement`),
  KEY `fk_Movement_Game1_idx` (`IDGame`),
  CONSTRAINT `fk_Movement_Game1` FOREIGN KEY (`IDGame`) REFERENCES `game` (`IDJogo`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB DEFAULT CHARSET = utf8 COLLATE = utf8_general_ci;

-- Data exporting was unselected.
-- Dumping structure for table marsami_game.occupation
CREATE TABLE IF NOT EXISTS `occupation` (
  `IDJogo` int(11) NOT NULL,
  `NumeroMarsamisOdd` int(11) NOT NULL,
  `NumeroMarsamisEven` int(11) NOT NULL,
  `Sala` int(11) NOT NULL,
  PRIMARY KEY (`IDJogo`),
  KEY `fk_Occupation_Game1_idx` (`IDJogo`),
  CONSTRAINT `fk_Occupation_Game1` FOREIGN KEY (`IDJogo`) REFERENCES `game` (`IDJogo`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB DEFAULT CHARSET = utf8 COLLATE = utf8_general_ci;

-- Data exporting was unselected.
-- Dumping structure for table marsami_game.sound
CREATE TABLE IF NOT EXISTS `sound` (
  `IDSound` int(11) NOT NULL AUTO_INCREMENT,
  `Sound` varchar(12) NOT NULL,
  `Hour` datetime NOT NULL,
  `IDGame` int(11) NOT NULL,
  PRIMARY KEY (`IDSound`),
  KEY `fk_Sound_Game1_idx` (`IDGame`),
  CONSTRAINT `fk_Sound_Game1` FOREIGN KEY (`IDGame`) REFERENCES `game` (`IDJogo`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB DEFAULT CHARSET = utf8 COLLATE = utf8_general_ci;

-- Data exporting was unselected.
-- Dumping structure for table marsami_game.user
CREATE TABLE IF NOT EXISTS `user` (
  `Username` varchar(50) NOT NULL,
  `Nome` varchar(100) DEFAULT NULL,
  `Telemovel` varchar(12) DEFAULT NULL,
  `Tipo` varchar(3) NOT NULL,
  `Email` varchar(50) NOT NULL,
  `Grupo` int(11) DEFAULT NULL,
  PRIMARY KEY (`Username`) USING BTREE,
  UNIQUE KEY `Email_UNIQUE` (`Email`),
  UNIQUE KEY `Cellphone_UNIQUE` (`Telemovel`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8 COLLATE = utf8_general_ci;

-- Data exporting was unselected.
/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;

/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;

/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;