# import os
import pymysql
# from  flask_mysqldb import MySQL
# from dotenv import load_dotenv
from config import Config
# load_dotenv()

# def get_connection():
#     connection = MySQL.connect(
#         host=os.getenv("MYSQL_HOST"),
#         user=os.getenv("MYSQL_USER"),
#         password=os.getenv("MYSQL_PASSWORD"),
#         database=os.getenv("MYSQL_DATABASE")
#         )
#     return connection
    
def get_connection():
    connection = pymysql.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DATABASE,
        port=Config.MYSQL_PORT,
        # ssl=Config.SSL
        ssl=Config.DB_SSL_CERTIFICATE,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )

    return connection