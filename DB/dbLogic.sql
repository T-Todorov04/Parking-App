USE `2024_TU_Lab1`; #TODO: Change Schema

# This will be executed, when camera scans car before entering the parking
DELIMITER $$
CREATE PROCEDURE IF NOT EXISTS car_entry(IN plate VARCHAR(15))
BEGIN
    DECLARE car_exists INT;

    -- Проверка дали колата вече съществува в базата
    SELECT COUNT(*) INTO car_exists
    FROM cars
    WHERE license_plate = plate;

    IF car_exists > 1 THEN
        SELECT 'Car already in DB' AS message;
    END IF;

    -- Ако не съществува, добави нов запис
    IF car_exists = 0 THEN
        INSERT INTO cars (license_plate, entry_time)
        VALUES (plate, NOW());
        SELECT 'Car added succeccfully' AS message;
    END IF;
END$$

DELIMITER ;
#CALL car_entry('PB3333BB');

#This will execute when car tries to leave the parking

DELIMITER $$
CREATE PROCEDURE car_exit(IN plate VARCHAR(15))
BEGIN
    DECLARE valid_exit INT;

    -- Проверка дали end_of_payment е в бъдещето или сега
    SELECT COUNT(*) INTO valid_exit
    FROM cars
    WHERE license_plate = plate
      AND end_of_payment >= NOW();

    IF valid_exit > 0 THEN
        SELECT 'Бариерата се отваря' AS message;
    ELSE
        SELECT 'Първо си плати' AS message;
    END IF;
END$$
DELIMITER ;

CALL car_exit('PA4444PA');

#This procedure calculates end_of_payment on the basis of time_of_payment and paid (how many days he has paid for)


DELIMITER $$
CREATE PROCEDURE update_payment(
    IN plate VARCHAR(15),
    IN days_paid INT
)
BEGIN
    -- Обновява последния запис на тази кола с ново време на плащане и край на плащане
    UPDATE cars
    SET
        time_of_payment = NOW(),
        end_of_payment = DATE_ADD(NOW(), INTERVAL days_paid DAY),
        paid = days_paid
    WHERE license_plate = plate
    ORDER BY entry_time DESC
    LIMIT 1;

    SELECT 'Плащането е регистрирано успешно' AS message;
END$$

DELIMITER ;
CALL update_payment('PA4444PA', 4);