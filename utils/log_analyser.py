import can
import pandas as pd
from collections import defaultdict

def load_log(file_path):
	messages = []
	with can.ASCReader(file_path) as log:
		for msg in log:
			messages.append([f"{msg.arbitration_id:03X}", msg.data.hex()])
	df = pd.DataFrame(messages,columns = ["ID", "Data"])
	return df
	
def compare_can_logs(file1,file2):
	df1 = load_can_log(file1)
	df2 = load_can_log(file2)
	
	grouped1 = df1.groupby("ID")["Data"].apply(list).to_dict()
	grouped2 = df2.groupby("ID")["Data"].apply(list).to_dict()
	
	differences = {}
	
	all_ids = sorted(set(grouped1.keys()).union(set(grouped2.keys())))
	
	for can_id in all_ids:
		data1 = grouped1.get(can_id, [])
		data2 = grouped2.get(can_id, [])
		
		data1_sorted = sorted(data1)
		data2_sorted = sorted(data2)
		
		if data1_sorted != data2_sorted:
			differences[can_id] = {
				"File 1": data1_sorted,
				"File 2": data2_sorted
			}
			
	return differences
	

file1 = "/home/mjt/fyp/Ford_In_A_Box/log_files/pcm/PCM_startup"
file2 = "/home/mjt/fyp/Ford_In_A_Box/log_files/pcm/PCM_startup_with_ig"

difference = compare_can_logs(file1, file2)

for can_id, diff in difference.items():
	print(f"\ndifferences for message ID: {can_id}")
	print("File 1: ", diff["File 1"])
	print("File 2: ", diff["File 2"])
