from utils.canbus import CanBus
import time 

with CanBus(channel = "can0", log_folder = r"log_files/full_system") as can0:
    try:
        while True:
            sent = can0.send(data = [0,0,0,0,0,0,0,0], arb_id = 0)
    except KeyboardInterrupt:
        pass
print("stopped")
 
 
