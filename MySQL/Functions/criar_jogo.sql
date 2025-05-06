DELIMITER //

CREATE DEFINER=`app`@`localhost` PROCEDURE `criar_jogo`(
	IN `username` VARCHAR(50),
	IN `game_description` VARCHAR(200),
	IN `game_name` VARCHAR(50),
	IN `number_marsamis` INT,
	IN `noise_tolerance` DOUBLE,
	IN `base_noise` DOUBLE
)
LANGUAGE SQL
NOT DETERMINISTIC
CONTAINS SQL
SQL SECURITY DEFINER
COMMENT ''
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
END //

DELIMITER ;
