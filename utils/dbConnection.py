import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root", 
        password="T31102004", 
        database="parkingCarsDB"  
    )
