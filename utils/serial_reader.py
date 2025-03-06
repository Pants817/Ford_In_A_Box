import serial
import time

class Ser:
	def __init__(self, port, baud_rate):
		while True:
			try:
				self.ser = serial.Serial(port,baud_rate)
				print(f"Serial connection created on {port} at {baud_rate} baud")
			except Exception as ew:
				print(f"Failed to create connection: {e}. Tring again in 1 second")
				time.sleep(1)
				
	def send(self, message:str):
		try:
			self.ser.write(message.encode('utf-8'))
		except Exception as e:
			print(f"Failed to write: {e}")
	
	def read(self):
		try:
			recv = self.ser.read()
			return recv
		except Exception as e:
			print(f"Failed to read: {e}")
			
	def close(self):
		self.ser.close()
		
	def __enter__(self):
		return self
		
	def __exit__(self, *args):
		self.close()
		
		
