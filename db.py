import psycopg2
from psycopg2 import Error

try:
    connection = psycopg2.connect(user="postgres",
                                  password="porcopaulo",
                                  host="127.0.0.1",
                                  port="5432",
                                  dbname="LoG")

    cursor = connection.cursor()

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)

def get_acc_names():
        try:
            cursor.execute("SELECT acc_name FROM accounts;")
            result = cursor.fetchall()
            cursor.close()
            return result
        except (Exception, Error) as error:
            print(error)
            return False

def insert_acc(acc_name, player_name):
        try:
            cursor.execute("INSERT INTO accounts(acc_name, player_name, created_on) VALUES ('{}', '{}', CURRENT_TIMESTAMP);".format(acc_name,player_name))
            connection.commit()
            
        except (Exception, Error) as error:
            print(error)
            
        