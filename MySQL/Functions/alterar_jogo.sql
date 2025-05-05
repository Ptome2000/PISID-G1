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
END //

DELIMITER ;