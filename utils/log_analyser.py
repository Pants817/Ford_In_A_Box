import can 
from collections import defaultdict

def parse_log(file_path):
    messages = defaultdict(list)
    
    with can.ASCReader(file_path, relative_timestamp=True) as log:
        for msg in log:
            messages[msg.arbitration_id].append({
                'timestamp': msg.timestamp,
                'data': msg.data.hex()
            })
    return messages

def list_can_ids(messages):
    print("Available CAN IDs in the log file:")
    for can_id in sorted(messages.keys()):
        print(hex(can_id))

def show_message_difference(messages, can_id):
    can_id = int(can_id, 16)
    if can_id not in messages:
        print(f"Message with ID {hex(can_id)} isn't in the file")
        return
    
    print(f"All different data for message {hex(can_id)}:")
    for entry in messages[can_id]:
        print(f"Timestamp: {entry['timestamp']}, Data: {entry['data']}")

if __name__ == "__main__":
    file_path = input("Enter a ASC CAN log file: ")
    messages = parse_log(file_path)
    
    list_can_ids(messages)  # Show available CAN IDs
    
    while True:
        can_id = input("Enter a CAN ID to check (in hex) or q to quit: ")
        if can_id == "q":
            break
        show_message_difference(messages, can_id)
