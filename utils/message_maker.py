import cantools
import cantools.database 
import can

db = cantools.database.load_file('C:\\Users\\Toby Heath\\Downloads\\ford_lincoln_base_pt.dbc')


# Get the message object by name or frame ID
message = db.get_message_by_name('BodyInfo_3_FD1')  # or db.get_message_by_frame_id(947)

# Create a dictionary with all signal names set to 0
signals = {signal.name: 0 for signal in message.signals}

signals["IgnKeyType_D_Actl"] = 2
signals["Key_In_Ignition_Stat"] = 1
signals["Ignition_Status"] = 8


# Encode the message
data = message.encode(signals)

print(data.hex())

print(can.Message(arbitration_id=0x3b3, is_extended_id=False, is_rx=False, data= data))