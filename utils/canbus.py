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

		self.stop_listening = False # used with the listen function to say when to stop
		
		self.channel = channel
		self.bus = can.Bus(channel = channel, interface = "socketcan", receive_own_messages = True)
		self.arb_id = arb_id
		self.start_time = time.time()
		
		if log_folder != None:
			timestamp = datetime.now().strftime("%d-%m-%y_%H-%M-%S")
			file_name = log_folder+"/log_"+timestamp
			self.logger = can.ASCWriter(file_name)
			self.printer = can.Printer()
			self.notifier = can.Notifier(self.bus, [self.logger, self.printer])
			print(file_name)
		
	def __enter__(self):
		return self
		
	def __exit__(self, *args):
		self.shutdown()
		print(f"{self.channel} closed")
		
	def create_message(self):
		#this could be used later but not sure if it is needed
		pass
	
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
		#if self.log_file:
		#	self.log_file.on_message_received(msg)
		return msg
			
	def send_periodic(self, data, period, arb_id=None, duration = None, callback = None):
		if len(data) > 8:
			raise IndexError("The message payload shouldn't be above 8")
		if arb_id == None:
			if self.arb_id == None:
				raise ValueError("The arb_id must be either passed into the send function or set when creating the Canbus object")
			arb_id = self.arb_id
		msg = can.Message(arbitration_id=arb_id, data=data, is_extended_id=False, is_error_frame=False, is_remote_frame=False, is_rx=False)
		#if self.log_file:
		#	self.log_file.on_message_received(msg)
		task = self.bus.send_periodic(msg, period, duration)
		return task
			
	def recv(self, arb_id = None, timeout = 0.2):
		"""
		Receives a CAN message
		
		:param arb_id: int the arbitration id of the message that is expected or None for the next message
		:param timeout: int how long the bus should wait for the message
		"""
		if arb_id  == None:
			response = self.bus.recv(timeout)
			#if self.log_file and response:
			#	self.log_file.on_message_received(response)
			return response
		else:
			delta_time = 0
			start_time = time.time()
			while delta_time < timeout:
				response = self.bus.recv(timeout)
				#if self.log_file and response:
				#	self.log_file.on_message_received(response)
				if response and response.id == arb_id:
					return response
				delta_time = time.time() - start_time
			return -1

	def listen(self):
		self.stop_listening = False
		while not self.stop_listening:
			response = self.recv()
			yield response

	def stop_listen(self):
		self.stop_listening = True

	def shutdown(self):
		"""
		Shutsdown the bus and stops logging
		"""
		self.bus.shutdown()
		if self.logger != None:
			self.notifier.stop()
			
	def add_filter(self, ID:int):
		self.bus.set_filters([{"can_id": ID, "can_mask": 0xFFF, "extended": False}])
		
	

