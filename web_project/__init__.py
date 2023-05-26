import multiprocessing
import logging
from time import sleep
from SX127x.LoRa import *
from SX127x.board_config import BOARD
 
BOARD.setup()
 
# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
 
class LoRaRcvCont(LoRa):
    def __init__(self, verbose=False):
        super(LoRaRcvCont, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)
        self.data_queue = multiprocessing.Queue()  # Queue for inter-process communication
 
    def start(self):
        logging.info("\nStarted...")
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)
 
        while True:
            sleep(0.5)
            rssi_value = self.get_rssi_value()
            status = self.get_modem_status()
            sys.stdout.flush()
 
    def on_rx_done(self):
        logging.info("\nReceived:")
        self.clear_irq_flags(RxDone=1)
        payload = self.read_payload(nocheck=True)
        data = bytes(payload).decode("utf-8", "ignore")
        logging.info(data)
        self.data_queue.put(data)  # Put the received data into the queue
        self.set_mode(MODE.SLEEP)
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)
 
 
def run_lora(data_queue):
    lora = LoRaRcvCont(verbose=False)
    lora.set_mode(MODE.STDBY)
    lora.set_pa_config(pa_select=1)
 
    try:
        logging.info(lora)
        lora.start()
    except KeyboardInterrupt:
        sys.stdout.flush()
        logging.info("")
        sys.stderr.write("KeyboardInterrupt\n")
    finally:
        sys.stdout.flush()
        logging.info("")
        lora.set_mode(MODE.SLEEP)
        BOARD.teardown()
 
 
if __name__ == "__main__":
    # Start the LoRa reception in a separate process
    data_queue = multiprocessing.Queue()  # Queue for inter-process communication
    process = multiprocessing.Process(target=run_lora, args=(data_queue,))
    process.start()
 
    # Configure logging to display messages on the terminal
    logger = logging.getLogger()
    logger.addHandler(logging.StreamHandler())
 
    # Continuously read data from the queue and display it on the terminal
    while True:
        if not data_queue.empty():
            data = data_queue.get()
            logging.info("Received data in Django process: %s", data)
        # Other code or operations in the Django process can be performed here
 
        # Add a small delay to avoid excessive CPU usage
        sleep(0.1)
