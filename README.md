# Ford_In_A_Box
Ford Fiesta in a box for final year project

This project allows for communication with ECUs over CAN. It has been tailored to be used on a Raspberry Pi and to communicate witht he IPC, BCM, PCM and Gateway Module of a Ford Fiesta Mk8.

The "module_Test" files are there to test on specific ECUs for example the IPC_Test turn the IPC into a rudimental clock using hte RPM and Speed to tell show the hours and minutes.

To run these files you will have to run the command: sudo ip link set can0 up type can bitrate 500000
To initialise the CAN bus.

The utils.canbus.py file holds the Canbus object that is used to send, recieve anf log CAN messages.

