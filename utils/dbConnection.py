import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # смени ако е различен
        password="твоят_парола",  # смени с твоята
        database="parking_db"  # или каквато е твоята база
    )
