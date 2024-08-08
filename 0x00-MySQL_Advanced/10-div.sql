-- SQL script that creates a function SafeDiv that divides first by second number or returns 0 if second number is equal to 0
DROP FUNCTION IF EXISTS SafeDiv;
DELIMITER $$
CREATE FUNCTION SafeDiv (a INT, b INT)
RETURNS FLOAT DETERMINISTIC
BEGIN
    DECLARE divresult FLOAT DEFAULT 0;

    IF b != 0 THEN
	SET divresult = a / b;
    END IF;
    RETURN divresult;
END $$
DELIMITER ;
