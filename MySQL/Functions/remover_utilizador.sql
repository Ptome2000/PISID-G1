CREATE DEFINER=`admin`@`localhost` PROCEDURE `remover_utilizador`(
    IN `userid` INT
)
SQL SECURITY DEFINER
BEGIN
    DELETE FROM `user`
    WHERE IDUser = userid;
END