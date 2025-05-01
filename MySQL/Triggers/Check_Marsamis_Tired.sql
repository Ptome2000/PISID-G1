create definer = root@localhost trigger Check_Marsamis_Tired
    after update
                     on Marsami
                     for each row
begin
    -- Declare variables for total Marsamis with CurrStatus = 2 and the game's TotalMarsamis
    DECLARE total_status_2 INT;
    DECLARE total_marsamis INT;

    -- Count Marsamis with CurrStatus = 2 for the corresponding GameID where GameOver = false
SELECT COUNT(*)
INTO total_status_2
FROM Marsami
WHERE CurrStatus = 2
  AND GameID = NEW.GameID
  AND GameID IN (
    SELECT IDJogo
    FROM Game
    WHERE GameOver = 0
);

-- Get the TotalMarsamis value from the Game table
SELECT TotalMarsamis
INTO total_marsamis
FROM Game
WHERE IDJogo = NEW.GameID
  AND GameOver = 0;

-- If the total matches, update the GameOver field to true
IF total_status_2 = total_marsamis THEN
UPDATE Game
SET GameOver = 1
WHERE IDJogo = NEW.GameID;
END IF;
end;

