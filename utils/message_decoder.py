import cantools
import cantools.database 

db = cantools.database.load_file('C:\\Users\\Toby Heath\\Downloads\\ford_lincoln_base_pt.dbc')
while True:
    id = int(input("Enter the ID: "),16)
    data = bytearray.fromhex(input("Enter the message data: "))

    message =  db.get_message_by_frame_id(id)
    print(f"BO_ {message.frame_id} {message.name}_{message.length}: {message.senders}")

    # Print each signal's definition
    for signal in message.signals:
        print(f"SG_ {signal.name} : {signal.start}|{signal.length}@{signal.byte_order}+ ({signal.scale},{signal.offset}) [{signal.minimum}|{signal.maximum}] \"{signal.unit}\"  {','.join(signal.receivers)}")
    
    print("\nshowing data breakdown\n")
    
    decoding = db.decode_message(id, data)
    
    for key, value in decoding.items():
        print(f"{key} = {value}")