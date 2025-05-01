create definer = root@localhost trigger Update_Marsami
    after insert
    on Movement
    for each row
begin
    -- Atualiza os campos CurrStatus e CurrRoom na tabela Marsami
UPDATE Marsami
SET CurrStatus = NEW.Status,
    CurrRoom = NEW.DestinationRoom
WHERE MarsamiNumber = NEW.MarsamiNum
  AND GameID = NEW.IDGame
  AND GameID IN (
    SELECT IDJogo
    FROM Game
    WHERE GameOver = 0
);
end;

