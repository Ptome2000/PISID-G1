DELIMITER //

CREATE DEFINER=`app`@`localhost` PROCEDURE `criar_utilizador`(
    IN `name` VARCHAR(100),
    IN `username` VARCHAR(50),
    IN `email` VARCHAR(50),
    IN `password` VARCHAR(64),
    IN `phone` VARCHAR(15)
)
SQL SECURITY DEFINER
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
END //

DELIMITER ;
