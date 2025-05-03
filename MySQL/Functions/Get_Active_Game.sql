CREATE PROCEDURE get_active_game(IN `user_name` VARCHAR(50))
BEGIN
    -- Esta função devolve o jogo ativo do utilizador
    SELECT *
    FROM Game
    WHERE Game.Username = user_name
      AND GameOver = 0
    LIMIT 1;
END