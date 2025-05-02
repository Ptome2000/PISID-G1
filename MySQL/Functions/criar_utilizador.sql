CREATE DEFINER=`app`@`localhost` PROCEDURE `criar_utilizador`(
    IN `name` VARCHAR(100),
    IN `username` VARCHAR(50),
    IN `email` VARCHAR(50),
    IN `password` VARCHAR(64),
    IN `phone` VARCHAR(15)
)
SQL SECURITY DEFINER
BEGIN
    -- Cria o utilizador MySQL com password fornecida
    SET @create_user = CONCAT('CREATE USER \'', username, '\'@\'localhost\' IDENTIFIED BY \'', password, '\';');
    PREPARE stmt FROM @create_user;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;

    -- Insere os dados na tabela da aplicação, sem password
    INSERT INTO `user` (`Nome`, `Username`, `Email`, `Telemovel`)
    VALUES (name, username, email, phone);
END