from utils.canbus import CanBus

with CanBus(channel = "can0", log_folder = r"log_files") as can0:
    try:
        while True:
            response = can0.recv()
            print(response)
    except KeyboardInterrupt:
        pass