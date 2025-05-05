DELIMITER //

CREATE DEFINER=`admin`@`localhost` PROCEDURE `remover_utilizador`(
    IN `in_username` INT
)
SQL SECURITY DEFINER
BEGIN
    DELETE FROM `user`
    WHERE Username = in_username;
END //

DELIMITER ;