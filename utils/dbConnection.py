import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # смени ако е различен
        password="T31102004",  # смени с твоята
        database="parkingCarsDB"  # или каквато е твоята база
    )
