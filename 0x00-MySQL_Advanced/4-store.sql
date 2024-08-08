-- SQL script that creates a trigger that decreases quantity of an item after adding new order
DROP TRIGGER IF EXISTS reduce_quantity;
DELIMETER $$
CREATE TRIGGER reduce_quantity
AFTE INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE items
        SET quantity = quantity - NEW.number
        WHERE name = NEW.item_name;
END $$
DELIMITER ;
