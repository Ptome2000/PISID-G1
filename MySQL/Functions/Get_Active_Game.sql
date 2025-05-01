CREATE PROCEDURE get_active_game(IN UserID INT)
BEGIN
    -- Check if there is any active game for the given UserID
    SELECT *
    FROM Game
    WHERE Game.UserID = UserID
      AND GameOver = 0
    LIMIT 1;
END