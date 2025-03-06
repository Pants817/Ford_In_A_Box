from utils.canbus import CanBus

with CanBus(channel = "can0", log_folder = r"log_files") as can0:
    while True:
        listener = can0.listen()
        response = next(listener)
        print(response)
        if response != None:
            if response.data == [0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01]:
                can0.send([0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01], arb_id = 0x001)
            elif response.data == [0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02]:
                can0.stop_listen()
