import os
from pathlib import Path
import time
import logging



# ====================================
# ========== Logging Config ==========
# ====================================

config_log_path = ""
Path(os.getenv("LOG_PATH")).mkdir(parents=True, exist_ok=True)
if os.getenv("LOGGING"):
    config_log_path = f"{{}}/{{}}.log".format(str(os.getenv("LOG_PATH")), time.strftime("%m%d%Y", time.localtime()))
else:
    config_log_path = "/dev/null"

logging.basicConfig(
    level=logging.INFO,
    filename=config_log_path,
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
)
