USE `parkingCarsDB`;
CREATE TABLE cars (
    id INT AUTO_INCREMENT PRIMARY KEY,
    license_plate VARCHAR(15) NOT NULL UNIQUE,
    entry_time DATETIME,
    time_of_payment DATETIME,
    end_of_payment DATETIME,
    paid INT DEFAULT 0
);


