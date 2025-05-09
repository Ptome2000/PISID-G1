-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.4.28-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             12.5.0.6677
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

-- Dumping structure for procedure marsami_game.alterar_jogo
DELIMITER //
CREATE DEFINER=`app`@`localhost` PROCEDURE `alterar_jogo`(
    IN `in_idjogo` VARCHAR(50),
    IN `in_name` VARCHAR(50),
    IN `in_description` VARCHAR(200)
)
BEGIN
    -- Altera os dados na tabela game
    UPDATE `game`
    SET `Description` = in_description,
        `GameName` = in_name
    WHERE `IDJogo` = in_idjogo;
END//
DELIMITER ;

-- Dumping structure for procedure marsami_game.alterar_utilizador
DELIMITER //
CREATE DEFINER=`app`@`localhost` PROCEDURE `alterar_utilizador`(
    IN `in_name` VARCHAR(100),
    IN `in_username` VARCHAR(50),
    IN `in_email` VARCHAR(50),
    IN `in_phone` VARCHAR(15)
)
BEGIN
    -- Altera os dados na tabela user
    UPDATE `user`
    SET `Nome` = in_name,
        `Email` = in_email,
        `Telemovel` = in_phone
    WHERE `Username` = in_username;
END//
DELIMITER ;

-- Dumping structure for procedure marsami_game.criar_jogo
DELIMITER //
CREATE DEFINER=`app`@`localhost` PROCEDURE `criar_jogo`(
	IN `username` VARCHAR(50),
	IN `game_description` VARCHAR(200),
	IN `game_name` VARCHAR(50),
	IN `number_marsamis` INT,
	IN `noise_tolerance` DOUBLE,
	IN `base_noise` DOUBLE
)
BEGIN
	UPDATE game SET GameOver = 1 WHERE Game.Username = username;
	INSERT INTO game (
		StartDate,
		GameOver,
        Username,
        Description,
        GameName,
        TotalMarsamis,
        SoundVarTolerance,
        BaseSound
    ) VALUES (
    	NOW(),
    	0,
        username,
        game_description,
        game_name,
        number_marsamis,
        noise_tolerance,
        base_noise
    );
END//
DELIMITER ;

-- Dumping structure for procedure marsami_game.criar_utilizador
DELIMITER //
CREATE DEFINER=`app`@`localhost` PROCEDURE `criar_utilizador`(
    IN `name` VARCHAR(100),
    IN `username` VARCHAR(50),
    IN `email` VARCHAR(50),
    IN `password` VARCHAR(64),
    IN `phone` VARCHAR(15)
)
BEGIN
    -- Cria o utilizador MySQL se não existir
    SET @create_user = CONCAT(
        'CREATE USER IF NOT EXISTS \'', username, '\'@\'localhost\' IDENTIFIED BY \'', password, '\';'
    );
    PREPARE stmt FROM @create_user;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;

    -- Dá permissão de leitura (SELECT) na base de dados marsami_game
    SET @grant_select = CONCAT(
        'GRANT SELECT ON marsami_game.* TO \'', username, '\'@\'localhost\';'
    );
    PREPARE stmt FROM @grant_select;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;

    -- Dá permissão de execução da procedure marsami_game.ver_dados
    SET @grant_proc1 = CONCAT(
        'GRANT EXECUTE ON PROCEDURE marsami_game.alterar_jogo TO \'', username, '\'@\'localhost\';'
    );
    PREPARE stmt FROM @grant_proc1;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;

    -- Insere os dados na tabela da aplicação
    INSERT INTO `user` (`Username`, `Nome`, `Telemovel`, `Tipo`, `Email`, `Grupo`)
    VALUES (username, name, phone, 'USR', email, 1);
END//
DELIMITER ;

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
  PRIMARY KEY (`IDJogo`),
  UNIQUE KEY `StartDate_UNIQUE` (`StartDate`),
  KEY `FK_game_user` (`Username`),
  CONSTRAINT `FK_game_user` FOREIGN KEY (`Username`) REFERENCES `user` (`Username`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8 COLLATE = utf8_general_ci;

-- Data exporting was unselected.

-- Dumping structure for procedure marsami_game.game_over
DELIMITER //
CREATE DEFINER=`app`@`localhost` PROCEDURE `game_over`(IN id_jogo INT)
BEGIN
    -- Esta função atualiza o estado do jogo para GameOver
    UPDATE game
        SET GameOver = 1
    WHERE IDJogo = id_jogo
      AND GameOver = 0;
END//
DELIMITER ;

-- Dumping structure for procedure marsami_game.get_active_game
DELIMITER //
CREATE DEFINER=`app`@`localhost` PROCEDURE `get_active_game`(
	IN `user_name` VARCHAR(50)
)   
BEGIN
	 SELECT *
    FROM Game
    WHERE Game.Username = user_name
      AND GameOver = 0
    LIMIT 1;
END//
DELIMITER ;

-- Dumping structure for table marsami_game.marsami
CREATE TABLE IF NOT EXISTS `marsami` (
  `IDMarsami` int(11) NOT NULL AUTO_INCREMENT,
  `MarsamiNumber` int(11) NOT NULL,
  `CurrStatus` enum('0','1','2') NOT NULL,
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
  `Leitura` decimal(6,2) DEFAULT NULL,
  `TipoAlerta` varchar(50) DEFAULT NULL,
  `Msg` varchar(100) DEFAULT NULL,
  `HoraEscrita` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`),
  KEY `fk_Message_Game1_idx` (`GameID`),
  CONSTRAINT `fk_Message_Game1` FOREIGN KEY (`GameID`) REFERENCES `game` (`IDJogo`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

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
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `IDJogo` int(11) NOT NULL,
  `NumeroMarsamisOdd` int(11) NOT NULL,
  `NumeroMarsamisEven` int(11) NOT NULL,
  `Sala` int(11) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `FK_occupation_game` (`IDJogo`),
  CONSTRAINT `FK_occupation_game` FOREIGN KEY (`IDJogo`) REFERENCES `game` (`IDJogo`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- Data exporting was unselected.

-- Dumping structure for procedure marsami_game.post_alert
DELIMITER //
CREATE DEFINER=`app`@`localhost` PROCEDURE `post_alert`(
    IN `Hora` datetime,
    IN `Sala` int(11),
    IN `GameID` int(11),
    IN `Sensor` int(11),
    IN `Leitura` decimal(6,2),
    IN `TipoAlerta` varchar(50),
    IN `Msg` varchar(100)
)
BEGIN
    DECLARE UltimoTipoAlerta VARCHAR(50);
	DECLARE UltimoGameID INT;

	SELECT m.TipoAlerta, m.GameID
	INTO UltimoTipoAlerta, UltimoGameID
	FROM message m
	ORDER BY m.id DESC
	LIMIT 1;

	IF UltimoGameID IS NULL OR (UltimoGameID != GameID OR UltimoTipoAlerta != TipoAlerta) THEN
	    INSERT INTO message (Hora, Sala, GameID, Sensor, Leitura, TipoAlerta, Msg, HoraEscrita)
	    VALUES (Hora, Sala, GameID, Sensor, Leitura, TipoAlerta, Msg, NOW());
	END IF;
END //
DELIMITER ;

-- Dumping structure for procedure marsami_game.remover_utilizador
DELIMITER //
CREATE DEFINER=`admin`@`localhost` PROCEDURE `remover_utilizador`(
    IN `in_username` INT
)
BEGIN
    DELETE FROM `user`
    WHERE Username = in_username;
END//
DELIMITER ;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- Data exporting was unselected.

-- Dumping structure for trigger marsami_game.Check_Marsamis_Tired
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_ZERO_IN_DATE,NO_ZERO_DATE,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE DEFINER=`admin`@`localhost` trigger Check_Marsamis_Tired
    after update
                     on Marsami
                     for each row
begin
    -- Declare variables for total Marsamis with CurrStatus = 2 and the game's TotalMarsamis
    DECLARE total_status_2 INT;
    DECLARE total_marsamis INT;

    -- Count Marsamis with CurrStatus = 2 for the corresponding GameID where GameOver = false
SELECT COUNT(*)
INTO total_status_2
FROM Marsami
WHERE CurrStatus = 2
  AND GameID = NEW.GameID
  AND GameID IN (
    SELECT IDJogo
    FROM Game
    WHERE GameOver = 0
);

-- Get the TotalMarsamis value from the Game table
SELECT TotalMarsamis
INTO total_marsamis
FROM Game
WHERE IDJogo = NEW.GameID
  AND GameOver = 0;

-- If the total matches, update the GameOver field to true
IF total_status_2 = total_marsamis THEN
UPDATE Game
SET GameOver = 1
WHERE IDJogo = NEW.GameID;
END IF;
end//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Dumping structure for trigger marsami_game.Update_Marsami
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_ZERO_IN_DATE,NO_ZERO_DATE,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE DEFINER=`admin`@`localhost` TRIGGER `Update_Marsami` AFTER INSERT ON `movement` FOR EACH ROW begin
-- Verifica se já existe um registo com o MarsamiNumber e GameID
    IF EXISTS (
        SELECT 1
        FROM Marsami
        WHERE MarsamiNumber = NEW.MarsamiNum
          AND GameID = NEW.IDGame
          AND GameID IN (
              SELECT IDJogo
              FROM Game
              WHERE GameOver = 0
          )
    ) THEN
        -- Atualiza os campos CurrStatus e CurrRoom na tabela Marsami
        UPDATE Marsami
        SET CurrStatus = NEW.Status,
            CurrRoom = NEW.DestinationRoom
        WHERE MarsamiNumber = NEW.MarsamiNum
          AND GameID = NEW.IDGame;
    ELSE
        -- Insere novo registo
        INSERT INTO Marsami (MarsamiNumber, GameID, CurrStatus, CurrRoom)
        VALUES (NEW.MarsamiNum, NEW.IDGame, NEW.Status, NEW.DestinationRoom);
    END IF;
end//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Dumping structure for trigger marsami_game.Update_Occupation_I
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_ZERO_IN_DATE,NO_ZERO_DATE,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE DEFINER=`admin`@`localhost` TRIGGER `Update_Occupation_I` AFTER INSERT ON `marsami` FOR EACH ROW begin
    -- Declare variables for even and odd counts
    DECLARE total_even INT;
    DECLARE total_odd INT;

    -- Count MarsamiNumber values that are even
SELECT COUNT(*)
INTO total_even
FROM Marsami
WHERE MOD(MarsamiNumber, 2) = 0
  AND GameID = NEW.GameID
  AND CurrRoom = NEW.CurrRoom
  AND GameID IN (
    SELECT IDJogo
    FROM Game
    WHERE GameOver = 0
);

-- Count MarsamiNumber values that are odd
SELECT COUNT(*)
INTO total_odd
FROM Marsami
WHERE MOD(MarsamiNumber, 2) <> 0
  AND GameID = NEW.GameID
  AND CurrRoom = NEW.CurrRoom
  AND GameID IN (
    SELECT IDJogo
    FROM Game
    WHERE GameOver = 0
);

IF EXISTS (
    SELECT 1
    FROM Occupation
    WHERE IDJogo = NEW.GameID
    AND Sala = NEW.CurrRoom
) THEN
    -- Atualiza se já existir
    UPDATE Occupation
    SET NumeroMarsamisEven = total_even,
        NumeroMarsamisOdd = total_odd
    WHERE IDJogo = NEW.GameID AND Sala = NEW.CurrRoom;
ELSE
    -- Insere se não existir
    INSERT INTO Occupation (IDJogo, NumeroMarsamisEven, NumeroMarsamisOdd, Sala)
    VALUES (NEW.GameID, total_even, total_odd, NEW.CurrRoom);
END IF;
end//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Dumping structure for trigger marsami_game.Update_Occupation_U
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_ZERO_IN_DATE,NO_ZERO_DATE,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE DEFINER=`admin`@`localhost` TRIGGER `Update_Occupation_U` AFTER UPDATE ON `marsami` FOR EACH ROW begin
    -- Declare variables for even and odd counts
    DECLARE total_even INT;
    DECLARE total_odd INT;

    -- Count MarsamiNumber values that are even
SELECT COUNT(*)
INTO total_even
FROM Marsami
WHERE MOD(MarsamiNumber, 2) = 0
  AND GameID = NEW.GameID
  AND CurrRoom = NEW.CurrRoom
  AND GameID IN (
    SELECT IDJogo
    FROM Game
    WHERE GameOver = 0
);

-- Count MarsamiNumber values that are odd
SELECT COUNT(*)
INTO total_odd
FROM Marsami
WHERE MOD(MarsamiNumber, 2) <> 0
  AND GameID = NEW.GameID
  AND CurrRoom = NEW.CurrRoom
  AND GameID IN (
    SELECT IDJogo
    FROM Game
    WHERE GameOver = 0
);

IF EXISTS (
    SELECT 1
    FROM Occupation
    WHERE IDJogo = NEW.GameID
    AND Sala = NEW.CurrRoom
) THEN
    -- Atualiza se já existir
    UPDATE Occupation
    SET NumeroMarsamisEven = total_even,
        NumeroMarsamisOdd = total_odd
    WHERE IDJogo = NEW.GameID AND Sala = NEW.CurrRoom;
ELSE
    -- Insere se não existir
    INSERT INTO Occupation (IDJogo, NumeroMarsamisEven, NumeroMarsamisOdd, Sala)
    VALUES (NEW.GameID, total_even, total_odd, NEW.CurrRoom);
END IF;
end//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
