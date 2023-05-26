#import django
from time import sleep
from SX127x.LoRa import *
from SX127x.board_config import BOARD
#import os
import threading

#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_project.settings')

#django.setup()
BOARD.setup()

class LoRaReceiver(LoRa):
    def __init__(self, verbose=False):
        super(LoRaReceiver, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)

    def start(self):
        print("\nStarted...")
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)

        while self.is_running:
            sleep(0.5)
            rssi_value = self.get_rssi_value()
            status = self.get_modem_status()
            sys.stdout.flush()

    def on_rx_done(self):
        print("\nReceived:")
        self.clear_irq_flags(RxDone=1)
        payload = self.read_payload(nocheck=True)
        data = bytes(payload).decode("utf-8", "ignore")
        print(data)
        self.set_mode(MODE.SLEEP)
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)


if __name__ == "__main__":
    lora = LoRaReceiver(verbose=False)
    lora.set_mode(MODE.STDBY)
    lora.set_pa_config(pa_select=1)

    try:
        print(lora)
        lora.is_running = True
        thread = threading.Thread(target=lora.start)
        thread.start()
        
        thread.join()
    except KeyboardInterrupt:
        sys.stdout.flush()
        print("")
        sys.stderr.write("KeyboardInterrupt\n")
    finally:
        sys.stdout.flush()
        print("")
        lora.is_running = False
        lora.set_mode(MODE.SLEEP)
        BOARD.teardown()
