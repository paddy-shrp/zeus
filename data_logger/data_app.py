import logging
import time

from mongo_db import MongoDB

from zeus_core.utils import settings
from zeus_core.utils import paths

logging.basicConfig(filename=paths.get_logs_path("data_app.log"), encoding="utf-8", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

set = settings.get_main_settings()["data_logger"]
uri = set["uri"].replace("<password>", set["password"])
mdb = MongoDB(uri)

def run_app():
    logging.info("Data Logger has been started")
    try:
        while True:
            mdb.log_modules()
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    logging.info("Data Logger has been stopped")

if __name__ == "__main__":
    run_app()