USE `2024_TU_Lab1`; #TODO: Change Schema

INSERT INTO cars (license_plate, entry_time, time_of_payment, end_of_payment, paid)
VALUES
('PA4444PA', '2025-07-21 12:00:00', NULL, NULL, 0),
('CA0001AA', '2025-07-21 11:30:00', '2025-07-21 11:45:00', '2025-07-22 11:45:00', 1),
('PB3333BB', '2025-07-20 23:59:59', '2025-07-21 00:00:00', '2025-07-24 00:00:00', 3);
