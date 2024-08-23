import functions_framework

import mysql.connector
from google.cloud.sql.connector import Connector
from mysql.connector import pooling
import os
from flask import escape,jsonify
import pytz
from datetime import datetime

# Create a connection pool
def create_pool():
    return pooling.MySQLConnectionPool(
        host='10.65.208.3',
        user=os.getenv('DB_USER'), # Database user from environment variables
        password=os.getenv('DB_PASSWORD'),  # Database password from environment variables
        database=os.getenv('DB_DATABASE'), # Database name from environment variables
        pool_size=2 # Set the pool size to 2 (the maximum number of connections in the pool)
    )


pool = create_pool()


def getRecommandedAddress(request):
    uid = request.args.get('uid')
    if not uid:
        return ('Missing uid parameter', 400)

    try:
        # Get a connection from the pool
        conn = pool.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM address_v2_training_data WHERE uid = %s"
        cursor.execute(query, (uid,))
        result = cursor.fetchall()

       

    except mysql.connector.Error as err:
        print("Error:", err)
        return ('Error connecting to the database or executing query', 500)

    finally:
        cursor.close()
        conn.close()

    return jsonify({"data": result})