DELIMITER //

CREATE DEFINER=`app`@`localhost` PROCEDURE `post_alert`(
    IN `Hora` datetime,
    IN `Sala` int(11),
    IN `Sensor` int(11),
    IN `Leitura` decimal(6,2),
    IN `TipoAlerta` varchar(50),
    IN `Msg` varchar(100)
)
BEGIN
    -- Insere os dados na tabela de mensagens
    INSERT INTO `message` (`Hora`, `Sala`, `Sensor`, `Leitura`,`TipoAlerta`,`Msg`)
    VALUES (Hora, Sala, Sensor, Leitura, TipoAlerta, Msg);
END //

DELIMITER ;