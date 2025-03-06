from utils.canbus import CanBus
import keyboard
import time

with CanBus(channel = "can1", log_folder = r"log_files") as can1:
	while True:
		time.sleep(0.4)
		can1.send(data = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00], arb_id = 0x001)
		if keyboard.is_pressed("q"):
			can1.send(data = [0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01], arb_id = 0x001)
			response = can1.recv()
			print(response)
		if keyboard.is_pressed("w"):
			can1.send(data = [0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02], arb_id = 0x001)
			response = can1.recv()
			print(response)
