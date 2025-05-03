CREATE DEFINER=`app`@`localhost` PROCEDURE `alterar_utilizador`(
    IN `name` VARCHAR(100),
    IN `username` VARCHAR(50),
    IN `email` VARCHAR(50),
    IN `password` VARCHAR(64),
    IN `phone` VARCHAR(15)
)
SQL SECURITY DEFINER
BEGIN
    -- Altera o utilizador MySQL com password fornecida
    SET @alter_user = CONCAT('CREATE USER \'', username, '\'@\'localhost\' IDENTIFIED BY \'', password, '\';');
    PREPARE stmt FROM @alter_user;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;

    -- Altera os dados na tabela user
    UPDATE `user`
    SET `Nome` = name,
        `Username` = username,
        `Email` = email,
        `Telemovel` = phone
    WHERE `Username` = username;
END