CREATE PROCEDURE get_active_game(IN UserID INT, OUT hasActiveGame BOOLEAN)
BEGIN
    -- Check if there is any active game for the given UserID
    SELECT EXISTS (
        SELECT 1
        FROM Game
        WHERE UserID = UserID
          AND GameOver = 0
    ) INTO hasActiveGame;
END