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


def create_tables():
    try:
        cursor.execute("""CREATE TABLE IF NOT EXISTS accounts (
                        	id serial PRIMARY KEY,
                            account_name VARCHAR ( 50 ) UNIQUE NOT NULL,
                            owner VARCHAR ( 50 ) NOT NULL,
                            created_on timestamp without time zone NULL);
                            
                          CREATE TABLE IF NOT EXISTS ranking (
                            id serial PRIMARY KEY,
                            positions jsonb
                          ); 
                        """)
        
        
        connection.commit()
        
    except (Exception, Error) as error:
        print(error)

    
create_tables()