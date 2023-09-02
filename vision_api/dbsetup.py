#pip install mysql-connector-python
import mysql.connector
import configparser
import sys, io


config = configparser.ConfigParser()
config.read(r'C:\Users\msong\Desktop\Bootcamp\bitcamp\Project KINNI\VisionAPI\vision_api\db_config.ini')

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')


def get_connection():
    
    #Extract database settings
    db_settings = config['database']

    return mysql.connector.connect(
        #Connect to the database 
        host = db_settings['host'],
        user = db_settings['user'],
        password = db_settings['password'],
        db = db_settings['db'],
        charset = db_settings['charset']
    )

