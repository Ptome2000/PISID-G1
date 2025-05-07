create definer = admin@localhost trigger Update_Occupation_U
    after update
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
  AND CurrRoom = NEW.CurrRoom
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
  AND CurrRoom = NEW.CurrRoom
  AND GameID IN (
    SELECT IDJogo
    FROM Game
    WHERE GameOver = 0
);

IF EXISTS (
    SELECT 1
    FROM Occupation
    WHERE IDJogo = NEW.GameID
    AND Sala = NEW.CurrRoom
) THEN
    -- Atualiza se já existir
    UPDATE Occupation
    SET NumeroMarsamisEven = total_even,
        NumeroMarsamisOdd = total_odd
    WHERE IDJogo = NEW.GameID AND Sala = NEW.CurrRoom;
ELSE
    -- Insere se não existir
    INSERT INTO Occupation (IDJogo, NumeroMarsamisEven, NumeroMarsamisOdd, Sala)
    VALUES (NEW.GameID, total_even, total_odd, NEW.CurrRoom);
END IF;
end;

