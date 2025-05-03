CREATE PROCEDURE get_active_game(IN username VARCHAR(50))
BEGIN
    -- Check if there is any active game for the given UserID
    SELECT *
    FROM Game
    WHERE Game.Username = username
      AND GameOver = 0
    LIMIT 1;
END