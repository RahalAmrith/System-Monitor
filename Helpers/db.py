import os
import sys
import mysql.connector
from .logging import logging

# ===============================
# ========== DB Config ==========
# ===============================

try:
    DB = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_DATABASE"),
        user=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD")
    )

    print("database connection: Success")
    logging.info("database connection: Success")

except mysql.connector.Error as e:
    print(e)
    logging.error(e)
    sys.exit()
