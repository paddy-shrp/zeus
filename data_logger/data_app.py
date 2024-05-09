import logging
import data_logger as dl
import utils.getters as getters
import time

logging.basicConfig(filename=getters.get_logs_path("data_app.log"), encoding="utf-8", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Log data every 15 Seconds? 
# Only log data when changes occur?

def run_app():
    logging.info("Data Logger has been started")
    try:
        while True:
            dl.log_data()
            time.sleep(15)
    except KeyboardInterrupt:
        pass
    logging.info("Data Logger has been stopped")

if __name__ == "__main__":
    run_app()