import psycopg2

connection = psycopg2.connect(
    database='password_keeper',
    user="postgres",
    password="z9djxxz0",
    host="127.0.0.1",
    port="5432"
)

cursor = connection.cursor()

