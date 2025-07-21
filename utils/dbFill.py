import random
from datetime import datetime, timedelta
from utils.dbConnection import get_connection

def generate_sample_cars(n=50):
    conn = get_connection()
    cursor = conn.cursor()

    for i in range(n):
        plate_prefix = random.choice([
            'A ', 'B ', 'BH', 'BP', 'BT', 'C ', 'CA', 'CB', 'CC', 'CH', 'CO', 'CT', 'E ', 'EB', 'EH', 'H ', 'KH', 'M ', 'E ', 'OB', 'P ', 'PA', 'PB', 'PE', 'PK', 'PP', 'T ', 'TX'])
        plate_number = f"{plate_prefix}{random.randint(1000, 9999)}{random.choice(['AB', 'AC', 'BA', 'BB'])}"

        if i < n // 2:
            # платени коли
            start_date = datetime(2025, 7, random.randint(1, 15))
            end_date = start_date + timedelta(days=random.randint(5, 20))
            cursor.execute(
                "INSERT INTO cars (license_plate, time_of_payment, end_of_payment) VALUES (%s, %s, %s)",
                (plate_number, start_date.date(), end_date.date())
            )
        else:
            # неплатени коли
            cursor.execute(
                "INSERT INTO cars (license_plate, time_of_payment, end_of_payment) VALUES (%s, NULL, NULL)",
                (plate_number,)
            )

    conn.commit()
    cursor.close()
    conn.close()
    print(f"{n} примерни коли са добавени успешно.")

if __name__ == "__main__":
    generate_sample_cars()
