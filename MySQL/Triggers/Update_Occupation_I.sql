create definer = admin@localhost trigger Update_Occupation_I
    after insert
    on Marsami
    for each row
begin
    -- Declare variables for even and odd counts
    DECLARE total_even INT;
    DECLARE total_odd INT;

    -- Count MarsamiNumber values that are even
SELECT COUNT(*)
INTO total_even
FROM Marsami
WHERE MOD(MarsamiNumber, 2) = 0
  AND GameID = NEW.GameID
  AND GameID IN (
    SELECT IDJogo
    FROM Game
    WHERE GameOver = 0
);

-- Count MarsamiNumber values that are odd
SELECT COUNT(*)
INTO total_odd
FROM Marsami
WHERE MOD(MarsamiNumber, 2) <> 0
  AND GameID = NEW.GameID
  AND GameID IN (
    SELECT IDJogo
    FROM Game
    WHERE GameOver = 0
);

-- Update the Occupation table with both counts
UPDATE Occupation
SET NumeroMarsamisEven = total_even,
    NumeroMarsamisOdd = total_odd
WHERE IDJogo = NEW.GameID;
end;

