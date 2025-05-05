DELIMITER //

CREATE DEFINER=`app`@`localhost` PROCEDURE `alterar_utilizador`(
    IN `in_name` VARCHAR(100),
    IN `in_username` VARCHAR(50),
    IN `in_email` VARCHAR(50),
    IN `in_phone` VARCHAR(15)
)
SQL SECURITY DEFINER
BEGIN
    -- Altera os dados na tabela user
    UPDATE `user`
    SET `Nome` = in_name,
        `Email` = in_email,
        `Telemovel` = in_phone
    WHERE `Username` = in_username;
END //

DELIMITER ;
