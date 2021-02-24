import psycopg2
from psycopg2 import Error

try:
    connection = psycopg2.connect(user="postgres",
                                  password="123",
                                  host="127.0.0.1",
                                  port="5432",
                                  dbname="LoG")

    cursor = connection.cursor()

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)

def get_acc_names():
    try:
        cursor.execute("SELECT account_name FROM accounts;")
        result = cursor.fetchall()
        return result
    except (Exception, Error) as error:
        print(error)
        return False

def insert_acc(account_name, owner_name):
    try:
        cursor.execute("INSERT INTO accounts(account_name, owner_name, created_on) VALUES ('{}', '{}', CURRENT_TIMESTAMP);".format(account_name,owner_name))
        connection.commit()
        
    except (Exception, Error) as error:
        print(error)
            
def insert_ranking(players_points):
    try:
        cursor.execute("INSERT INTO ranking(positions) VALUES ('{}');".format(players_points))
        connection.commit()
    except (Exception, Error) as error:
        print(error)