create definer = admin@localhost trigger Update_Marsami
    after insert
    on Movement
    for each row
begin
  -- Verifica se já existe um registo com o MarsamiNumber e GameID
    IF EXISTS (
        SELECT 1
        FROM Marsami
        WHERE MarsamiNumber = NEW.MarsamiNum
          AND GameID = NEW.IDGame
          AND GameID IN (
              SELECT IDJogo
              FROM Game
              WHERE GameOver = 0
          )
    ) THEN
        -- Atualiza os campos CurrStatus e CurrRoom na tabela Marsami
        UPDATE Marsami
        SET CurrStatus = NEW.Status,
            CurrRoom = NEW.DestinationRoom
        WHERE MarsamiNumber = NEW.MarsamiNum
          AND GameID = NEW.IDGame;
    ELSE
        -- Insere novo registo
        INSERT INTO Marsami (MarsamiNumber, GameID, CurrStatus, CurrRoom)
        VALUES (NEW.MarsamiNum, NEW.IDGame, NEW.Status, NEW.DestinationRoom);
    END IF;
end;

