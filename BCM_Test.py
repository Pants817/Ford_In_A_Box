from utils.canbus import CanBus
import time 

with CanBus(channel = "can0", log_folder = r"log_files/bcm/lock_testing/ids") as can0:
    try:
        can0.add_filter(0x3eb)
        while True:
            pass
            #response = can0.recv()
            #if response != None: print(response)
            #if time.time() - start > 0.5:
                #ignition_data = [0x40, 0x00,0x00, 0x80, 0x00,0x00,0x00,0x00]
                #sent = can0.send(data = ignition_data, arb_id = 0x3b2)
                #print(sent)
                #start = time.time()
    except KeyboardInterrupt:
        pass
print("stopped")
 
 
