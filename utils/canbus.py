import can
from datetime import datetime
import time
import threading
import os


class CanBus:
	def __init__(self, channel:str, arb_id:int = None, log_folder:str = None):
		"""
		Creates a python-can bus to send and receive CAN messages using Socketcan. It also creates a asc style log file of the messages.
		
		:param arb_id: int defualt arbitration id or None if it will change each message
		:param log_folder: str the folder for the log files or None if not logging
		:param channel: str which channel will be used on the pi
		"""
		if log_folder == None:
			self.log_file = None
		else:
			timestamp = datetime.now().strftime("%d-%m-%y_%H-%M-%S")
			file_name = log_folder+"/log_"+timestamp
			self.log_file = can.ASCWriter(file_name)
			print(file_name)
		
		self.channel = channel
		self.bus = can.ThreadSafeBus(channel = channel, interface = "socketcan")
		self.arb_id = arb_id
		
	def __enter__(self):
		return self
		
	def __exit__(self, *args):
		self.shutdown()
		print(f"{self.channel} closed")
	
	def send(self, data, arb_id = None, is_extended = False, is_error=False, is_remote=False):
		"""
		Sends a CAN message
		
		:param data: [int] the mssage payload
		:param arb_id: int the arbitration id of the message
		:param is_extended: bool if the message uses extended id
		:param is_error: bool if the message is an error message
		:param is_remote: if the message is a remote frame
		"""
		if len(data) > 8:
			raise IndexError("The message payload shouldn't be above 8")
		if arb_id == None:
			if self.arb_id == None:
				raise ValueError("The arb_id must be either passed into the send function or set when creating the Canbus object")
			arb_id = self.arb_id
		msg = can.Message(arbitration_id=arb_id, data=data, is_extended_id=is_extended, is_error_frame=is_error, is_remote_frame=is_remote, is_rx=False)
		self.bus.send(msg)
		if self.log_file:
			self.log_file.log_event(msg)
			
	def recv(self, arb_id = None, timeout = 0.2):
		"""
		Receives a CAN message
		
		:param arb_id: int the arbitration id of the message that is expected or None for the next message
		:param timeout: int how long the bus should wait for the message
		"""
		if arb_id  == None:
			response = self.bus.recv(timeout)
			if self.log_file and response:
				self.log_file.log_event(response)
			return response
		else:
			delta_time = 0
			start_time = time.time()
			while delta_time < timeout:
				response = self.bus.recv(timeout)
				if self.log_file and response:
					self.log_file.log_event(response)
				if response and response.id == arb_id:
					return response
				delta_time = time.time() - start_time
			return -1
			
	def shutdown(self):
		"""
		Shutsdown the bus and stops logging
		"""
		self.bus.shutdown()
		if self.log_file != None:
			self.log_file.stop()
		
	

