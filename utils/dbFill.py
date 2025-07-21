import random
from datetime import datetime, timedelta
from utils.dbConnection import get_connection

def generate_sample_cars(n=50):
    conn = get_connection()
    cursor = conn.cursor()

    for i in range(n):
        plate_prefix = random.choice([
            'A ', 'B ', 'BH', 'BP', 'BT', 'C ', 'CA', 'CB', 'CC', 'CH', 'CO', 'CT',
            'E ', 'EB', 'EH', 'H ', 'KH', 'M ', 'OB', 'P ', 'PA', 'PB', 'PE', 'PK', 'PP', 'T ', 'TX'
        ])
        plate_number = f"{plate_prefix}{random.randint(1000, 9999)}{random.choice(['BH', 'BP', 'BT', 'CA', 'CB', 'CC', 'CH', 'CO', 'CT', 'EB', 'EH', 'KH', 'OB', 'PA', 'PB', 'PE', 'PK', 'PP', 'TX'])}"

        today = datetime(2025, 7, 21)

        entry_time = today - timedelta(days=random.randint(0, 10), hours=random.randint(0, 23), minutes=random.randint(0, 59))

        if i < n // 3:
            payment_date = entry_time - timedelta(days=random.randint(5, 10))
            end_date = payment_date + timedelta(days=random.randint(1, 3))  
            cursor.execute(
                "INSERT INTO cars (license_plate, entry_time, time_of_payment, end_of_payment) VALUES (%s, %s, %s, %s)",
                (plate_number, entry_time, payment_date, end_date)
            )
        elif i < (2 * n) // 3:
            payment_date = entry_time
            end_date = payment_date + timedelta(days=random.randint(5, 20))
            cursor.execute(
                "INSERT INTO cars (license_plate, entry_time, time_of_payment, end_of_payment) VALUES (%s, %s, %s, %s)",
                (plate_number, entry_time, payment_date, end_date)
            )
        else:
            cursor.execute(
                "INSERT INTO cars (license_plate, entry_time, time_of_payment, end_of_payment) VALUES (%s, %s, NULL, NULL)",
                (plate_number, entry_time)
            )

    conn.commit()
    cursor.close()
    conn.close()
    print(f"{n} примерни коли са добавени успешно.")

if __name__ == "__main__":
    generate_sample_cars()
