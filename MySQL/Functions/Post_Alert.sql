DELIMITER //

CREATE DEFINER=`app`@`localhost` PROCEDURE `post_alert`(
    IN `Hora` datetime,
    IN `Sala` int(11),
    IN `GameID` int(11),
    IN `Sensor` int(11),
    IN `Leitura` decimal(6,2),
    IN `TipoAlerta` varchar(50),
    IN `Msg` varchar(100)
)
BEGIN
    DECLARE UltimoTipoAlerta VARCHAR(50);
	DECLARE UltimoGameID INT;

	SELECT m.TipoAlerta, m.GameID
	INTO UltimoTipoAlerta, UltimoGameID
	FROM message m
	ORDER BY m.id DESC
	LIMIT 1;

	IF UltimoGameID IS NULL OR (UltimoGameID != GameID OR UltimoTipoAlerta != TipoAlerta) THEN
	    INSERT INTO message (Hora, Sala, GameID, Sensor, Leitura, TipoAlerta, Msg, HoraEscrita)
	    VALUES (Hora, Sala, GameID, Sensor, Leitura, TipoAlerta, Msg, NOW());
	END IF;
END //

DELIMITER ;