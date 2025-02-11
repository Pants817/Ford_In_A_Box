from utils.canbus import CanBus

with CanBus(channel = "can0", log_folder = r"log_files") as can0:
    try:
        can0.send_periodic(data = [0x40, 0x00,0x00, 0x80, 0x00,0x00,0x00,0x00],period = 0.5, arb_id = 0x3b3, )
        while True:
            response = can0.recv()
            print(response)
    except KeyboardInterrupt:
        pass
print("stopped")
