CREATE PROCEDURE get_active_game(IN UserID INT, OUT ActiveGame INT)
BEGIN
    -- Check if there is any active game for the given UserID
    SELECT IDJogo
    INTO ActiveGame
    FROM Game
    WHERE Game.UserID = UserID
      AND GameOver = 0
    LIMIT 1;
END