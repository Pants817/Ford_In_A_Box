import can
from datetime import datetime

timestamp = datetime.now()
timestamp = timestamp.strftime("%d-%m-%y_%H-%M-%S")

log_folder = r"log_files"
file_name = log_folder+"/log_"+timestamp

print(file_name)

log_file = can.ASCWriter(file_name)

can0 = can.interface.Bus(channel='can0', bustype='socketcan')

msg = can.Message(is_extended_id=False, arbitration_id=0x3b3, data=[0x14, 0x00, 0x00, 0x0c, 0xe6, 0x00, 0x00, 0x00])


try:
	while True:
		#can0.send(msg)
		#log_file.log_event(msg)
		response = can0.recv(0.2)
		print(response)
		log_file.log_event(response)
except KeyboardInterrupt:
	can0.shutdown()
	log_file.stop()

