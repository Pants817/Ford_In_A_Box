from utils.canbus import CanBus

with CanBus(channel = "can0", log_folder = r"log_files") as can0:
    try:
        while True:
            can0.send([0x14, 0x00, 0x00, 0x0c, 0xe6, 0x00, 0x00, 0x00], 0x3b3)
            response = can0.recv()
            print(response)
    except KeyboardInterrupt:
        pass