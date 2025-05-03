CREATE PROCEDURE game_over(IN id_jogo INT)
BEGIN
    -- Esta função atualiza o estado do jogo para GameOver
    UPDATE game
        SET GameOver = 1
    WHERE IDJogo = id_jogo
      AND GameOver = 0;
END