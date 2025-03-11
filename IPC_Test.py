from utils.canbus import CanBus
from utils.serial_reader import Ser
import time

#Timings
WAKE_TIMEOUT = 0.5 # stay awake signal needed every 0.5 seconds

#IDs
WAKE_ID = 0x591
IGNITION_ID = 0x3B2
RPM_ID = 0x42F
SPEED_ID = 0x202
COOLENT_ID = 0x156
AIRBAG_ID = 0x04c
#Data
WAKE_DATA = [0x91,0x00,0xff,0xff,0xff,0xff,0xff,0xff]
AIRBAG_DATA = [0x00,0x55,0x55, 0x00, 0x00, 0x00, 0x00, 0x00] # turns off the Airbag symbol

#Clock
UNIT_PER_HOUR = 8000
UNIT_PER_MINUTE = 140
MINUTES_PER_UNIT_HOUR = 60 / (UNIT_PER_HOUR/UNIT_PER_MINUTE)

def get_rpm_message_data(rpm):
    if rpm < 0:
        rpm = 0
    scaled_rpm = int(rpm * 0.935)
    rpm_gate = 96+ int(scaled_rpm / 500)
    finetune = int((scaled_rpm % 500)/2)
    if rpm_gate >115:
        rpm_gate = 115
        
    return [0x00,0x00,0x00,0x00,0x00,0x00, rpm_gate, finetune]
	
def get_speed_message_data(mph, counter): # need to tweek this speed calc for mph
    speed = mph * 1.609
    ogspeed = speed
    speed = (speed / 2.66)
    finetune = ((speed*3)-ogspeed) * 10
    finetune = finetune - finetune % 100
    return [0x40,0x00,0x00,0x00,counter,counter, int(speed), int(finetune)]
    
def get_coolent_message_data(temp):#105 is the lowest equivilannt to 60 degrees 180 seems like the highest (its the highest value that doesn't trigger the icon)
    return [temp,0x00,0x00,0x00,0x23,0x00,0x00,0x00]
    
def calc_time():
    current_time = time.localtime()
    hour = current_time.tm_hour
    minute = current_time.tm_min
    second = current_time.tm_sec
    
    scaled_hour = (hour % 12) * (UNIT_PER_HOUR / 12)
    scaled_minute = (minute * UNIT_PER_MINUTE) / 60
    
    return int(scaled_hour), int(scaled_minute), int(second)
    
def start(can):
    sent = can.send(data = WAKE_DATA, arb_id=WAKE_ID)
    ignition_data = [0x40, 0x00,0x00, 0x80, 0x00,0x00,0x00,0x00]
    sent = can0.send(data = ignition_data, arb_id = IGNITION_ID)
    time.sleep(6)

    


with CanBus(channel = "can0", log_folder = r"log_files/ipc/demo") as can0:
    print("Press the enter button to start...")
    input()
    print("Starting")
    start(can0)
    #can0.send_periodic(data = WAKE_DATA,period = WAKE_TIMEOUT, arb_id=WAKE_ID) # This is needed still. It will die without it 
    second_switch = True
    #ignition_data = [0x40, 0x00,0x00, 0x80, 0x00,0x00,0x00,0x00]
    #sent = can0.send(data = ignition_data, arb_id = IGNITION_ID)
    print("starting loop")
    try:
        while True:
            hour , minute, second= calc_time()            
            ignition_data = [0x40, 0x00,0x00, 0x80, 0x00,0x00,0x00,0x00]
            sent = can0.send(data = ignition_data, arb_id = IGNITION_ID) # This is always needed none of the other commands work without it 
            rpm_data = get_rpm_message_data(hour)
            sent = can0.send(data = rpm_data, arb_id = RPM_ID)
            speed_data = get_speed_message_data(minute,65)
            sent = can0.send(data = speed_data, arb_id = SPEED_ID)
            coolent_data = get_coolent_message_data(100 if second_switch else 180)
            #coolent_data = get_coolent_message_data(140)
            sent = can0.send(data = coolent_data, arb_id = COOLENT_ID)
            second_switch = not second_switch
            sent = can0.send(data = AIRBAG_DATA, arb_id = AIRBAG_ID) # gets rid of the airbag warning
            alarm_brake_data = [0x00, 0x00, 0x00,0x00,0x00,0x00,0x00,0x00] # if 4th byte 0xff then the beeping will continue indefinitly. byte 2 and 3 don't seem to make a change <- this may be wrong I think need the abs message as well
            sent = can0.send(data = alarm_brake_data, arb_id = 0x3c3)
            abs_data = [0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00] # 6th byte is the tc 0x04 for flash, 0x02 for solid. 7th byte is abs 0x80 for flash 0x40 for solid
            sent = can0.send(data= abs_data, arb_id = 0x416)
            tpm_data = [0x31, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00] # comes up on the screen with the tire pressures and turns of the light. (not sure how to give it different tire pressures)
            sent = can0.send(data = tpm_data, arb_id = 0x3b4)
            oil_data = [0x08,0x00,0x00,0x00,0x00,0x00,0x00,0x00] # this turns off the oil symbol (haven't found which will make it flash or show up)
            sent = can0.send(data = oil_data, arb_id = 0x421)
            charge_data = [0x00,0x00,0xA6,0x00,0x00,0x00,0x00,0x00] # needs A6 in the 3rd byte. the second byte will decide if the charge light is on or not (0x11 is on, 0x00 is off)
            sent = can0.send(data = charge_data, arb_id = 0x42c)
            power_steering_data = [0x23,0x00,0x00,0x00,0x00,0x00,0x00,0x00] # 1st byte of 0x23 stops the message coming up on the screen 
            sent = can0.send(data = power_steering_data, arb_id = 0x877)
            language_data = [0x41, 0x11, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00] # 0x41 in the 1st byte is km and celsius 0x11 in second is english 0x23 is German
            sent = can0.send(data= language_data, arb_id = 0x191)
            outside_temp_data = [0x00,0x00,0x00,0x00,0x96,0x00,0xFF,0x00] # 5th byte is the temp 125 = 22c Need to find the conversion 100 = 10c, 150 = 35c
            sent = can0.send(data = outside_temp_data, arb_id = 0x3b3)
            front_camera_data = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00] # stops the message (would be very cool if I can get a camera hooked up)
            sent = can0.send(data = front_camera_data, arb_id = 0x3d8)
            lights_data = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00] # 8th byte is for the light 0x30 = highbeams 
            sent = can0.send(data = lights_data, arb_id = 0x46b)
            
            #response = can0.recv()
            #print(response)
            time.sleep(1)
    except KeyboardInterrupt:
        pass
