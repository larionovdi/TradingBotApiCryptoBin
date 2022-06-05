import psycopg2
from config import hostname, database, username, pwd, port_id







def connect_to_sql(data):
    try:
        connection = psycopg2.connect(
                host = hostname,
                dbname = database,
                user = username,
                password = pwd,
                port = port_id
        ) 
        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT version();'
            )
            print(f'Server version: {cursor.fetchone()}')
        
                            
                                

    except Exception as error:
        print(error)

    finally: 
        if connection:
            connection.close()
            print('[INFO] postgresql connection closed')
    




