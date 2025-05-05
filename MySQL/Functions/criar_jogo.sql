DELIMITER //

CREATE DEFINER=`app`@`localhost` PROCEDURE `criar_jogo`(
    IN `in_username` VARCHAR(50),
    IN `in_name` VARCHAR(50),
    IN `in_description` VARCHAR(200)
)
BEGIN
    -- Insere os dados na tabela game
    INSERT INTO `game` (`Username`, `GameName`, `Description`)
    VALUES (in_username, in_name, in_description);

END //

DELIMITER ;
