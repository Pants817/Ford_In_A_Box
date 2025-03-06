from utils.canbus import CanBus
import time

with CanBus(channel = "can0", log_folder = r"log_files/pcm/lock_testing") as can0:
    can_id = 0x580
    counter = 0x00
    ign_id = 0x3b2
    start = time.time()
    try:
        while True:
            response = can0.recv()
            print(response)
            #if time.time() - start > 1:
             #   ignition_data = [0x40, 0x00,0x00, 0x80, 0x00,0x00,0x00,0x00]
              #  sent = can0.send(data = ignition_data, arb_id = 0x3b2)
               # print(sent)
                #start = time.time()
            #wake_up = [counter, 0x00, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff]
            #sent = can0.send(data = wake_up, arb_id = can_id+counter)
            #print(hex(can_id+counter))
            #counter+=1
            #time.sleep(0.5)
    except KeyboardInterrupt:
        pass
