from utils.canbus import CanBus
import time 

with CanBus(channel = "can0", log_folder = r"log_files/full_system") as can0:
    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass
print("stopped")
 
 
