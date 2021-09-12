import os
import sys
import requests
from dotenv import load_dotenv
import time
import threading
import traceback

# setup env variables
load_dotenv()

# helpers
from Helpers.logging import logging
from Helpers.db import DB

# Model
from Models.Prdouct import Product_Model

# set time for script
time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

# HTTP Headers
HTTP_Headers = {"user-agent": "ilabs-alerts-1.0"}


# Functions
def ProcessProduct(product):
    p_hcu_total = 0
    p_hcu_success = 0
    p_hcu_fail = 0
    p_hcu_failed_urls = []
    p_hcu_latency = 0
    p_robots_status = 0
    p_robots_match_status = False

    # check for robots content

    try:
        robots_response = requests.get(f"{product['base_url']}/robots.txt", headers=HTTP_Headers)

        p_robots_status = int(robots_response.status_code)

        filtered_text = str(robots_response.content).replace("\n","")
        print(filtered_text)
        print(str(product['robots_content']).strip())

        if robots_response.content.strip() == product['robots_content'].strip():
            print(f"{product['base_url']} : robots match success")

    except Exception as e:
        print(e)
        logging.error(e)

    try:
        cur = DB.cursor(dictionary=True)
        cur.execute(Product_Model["getHealthCheckUrlsForProduct"], (product["id"],))
        HCUList = cur.fetchall()
        cur.close()

        print(f"{len(HCUList)} helath check ulrs fetched for {product['base_url']}")
        logging.info(f"{len(HCUList)} helath check ulrs fetched for {product['base_url']}")

    except Exception as e:

        print(e)
        logging.error(e)
        sys.exit()


print("Script started")
logging.info("Script started")

# Fetch Products
try:
    cur = DB.cursor(dictionary=True)
    cur.execute(Product_Model["getAllProducts"])
    ProductList = cur.fetchall()
    cur.close()

    print(f"{len(ProductList)} products fetched")
    logging.info(f"{len(ProductList)} products fetched")

except Exception as e:
    print(e)
    logging.error(e)
    sys.exit()

# Loop through each Products

for product in ProductList:
    ProcessProduct(product)

# try:
#     no_threads = int(os.getenv("THREAD_COUNT"))
#     thread_interval = int(os.getenv("THREAD_INTERVAL"))
#
#     threads = []
#
#     for product in ProductList:
#         while len(threading.enumerate()) > no_threads:
#             pass
#         thread1 = threading.Thread(
#             target=ProcessProduct,
#             kwargs={"product": product},
#         )
#         thread1.start()
#         threads.append(thread1)
#         time.sleep(thread_interval)
#
#     for t in threads:
#         t.join()
#
# except Exception as e:
#     print(traceback.print_exc())
#     logging.error(traceback.print_exc())


# closing DB connection
DB.close()
