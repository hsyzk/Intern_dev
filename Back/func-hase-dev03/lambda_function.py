import json
import pymysql
import os

def lambda_handler(event, context):
    
    endpoint = os.environ['db_endpoint']
    username = os.environ['db_username']
    password = os.environ['db_password']
    dbname = os.environ['db_name']
    
    conn = pymysql.connect(
            database = dbname,
            user = username,
            password = password,
            host = endpoint
    )
    cur = conn.cursor()
    
    try:
        cur.execute("select product_id, product_name from product")
        records = cur.fetchall()
        
        products = [{"product_id": record[0], "product_name": record[1]} for record in records]
        
        return {
            'statusCode': 200,
            'body': products
        }
    finally:
        cur.close()
        conn.close()