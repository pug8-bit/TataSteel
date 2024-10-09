import pyads
import struct
import time

# Constants for the message format
ENVELOPE_BEGIN_CHAR = 60  # '<' character used to mark the beginning of a message
ENVELOPE_BEGIN_KEY = 12345  # 4-byte key to signify the start of the message
ENVELOPE_END_KEY = 2 * ENVELOPE_BEGIN_KEY  # 4-byte key to signify the end of the message
ENVELOPE_END_CHAR = 62  # '>' character used to mark the end of a message
MESSAGESIZE_MAX = 2047  # Maximum allowed message size (in bytes)
COMMUNICATIONSTATUS_READYFORNEWCOMMAND = 1  # Communication ready status indicator
COMMUNICATIONSTATUS_EXECUTEDREADYFORNEWCOMMAND = 2  # Execution complete and ready for new command
COMMUNICATIONSTATUS_NEWCOMMANDAVAILABLE = 3  # New command available for execution
COMMAND_STATUS_EXECUTEDREADYFORNEWCOMMAND = 4  # Command executed and ready for new command

# Function to read the current communication status from the PLC
def read_communication_status(plc):
    status = plc.read_by_name("GVL_TcpCommunication.G_wCommunicationStatus", pyads.PLCTYPE_UINT)
    return status

# Function to check if the communication status indicates the PLC is ready for a new command
def wait_for_communication_status(plc):
    communication_status = read_communication_status(plc)
    return communication_status in [
        COMMUNICATIONSTATUS_EXECUTEDREADYFORNEWCOMMAND,
        COMMAND_STATUS_EXECUTEDREADYFORNEWCOMMAND
    ]

# Function to wait for the communication status to become ready, with a 5-second timeout
def wait_for_communication_status_5(plc, timeout=5):
    start_time = time.time()  # Start timer for timeout
    while time.time() - start_time < timeout:  # Loop until the timeout is reached
        # Read the current communication status
        communication_status = plc.read_by_name("GVL_TcpCommunication.G_wCommunicationStatus", pyads.PLCTYPE_UINT)
        # Check if the communication is ready for new commands
        if communication_status in [
            COMMUNICATIONSTATUS_EXECUTEDREADYFORNEWCOMMAND,
            COMMAND_STATUS_EXECUTEDREADYFORNEWCOMMAND
        ]:
            return True
        read_communication_status(plc)  # Re-read the status to ensure up-to-date information
        time.sleep(0.05)  # Wait for 50ms before the next check
    return False  # Timeout reached without communication readiness

# Function to send a message to the PLC
def send_message(plc, intArrayMessage):
    if wait_for_communication_status(plc):  # Wait until communication is ready
        try:
            message_size = 4 * len(intArrayMessage)  # Calculate message size in bytes
            envelope = bytearray()  # Create a bytearray to hold the message

            # Add the envelope's beginning character and key
            envelope.append(ENVELOPE_BEGIN_CHAR)
            envelope.extend(struct.pack('<I', ENVELOPE_BEGIN_KEY))

            # Add the message size
            envelope.extend(struct.pack('<I', message_size))

            # Pack each integer in the message array into the envelope
            for intItem in intArrayMessage:
                envelope.extend(struct.pack('i', intItem))

            # Add the envelope's end key and character
            envelope.extend(struct.pack('<I', ENVELOPE_END_KEY))
            envelope.append(ENVELOPE_END_CHAR)

            # Write the envelope to the PLC's memory
            for i in range(len(envelope)):
                plc.write_by_name(f"GVL_TcpCommunication.G_aTcpReceivedArea[{i}]", envelope[i], pyads.PLCTYPE_BYTE)

            print("Message sent successfully!")  # Print a success message
            # Update the PLC communication status
            plc.write_by_name("GVL_TcpCommunication.G_wCommunicationStatus", 1, pyads.PLCTYPE_DWORD)

            return True  # Indicate success in sending the message

        except Exception as e:  # Handle any errors during the sending process
            print(f"Error during send_message: {e}")
        return False  # Indicate failure in sending the message

# Function to read a message from the PLC
def read_message(plc):
    if wait_for_communication_status_5(plc):  # Wait until communication is ready with a 5s timeout
        try:
            envelope = bytearray()  # Create a bytearray to store the received message

            # Read message bytes from the PLC memory
            for i in range(MESSAGESIZE_MAX):
                byte = plc.read_by_name(f"GVL_TcpCommunication.G_abTcpSendArea[{i}]", pyads.PLCTYPE_BYTE)
                envelope.append(byte)

            # Validate that the message has the correct beginning character
            if envelope[0] != ENVELOPE_BEGIN_CHAR:
                raise ValueError("Invalid message format: Missing begin character.")

            # Validate the beginning key of the message
            begin_key = struct.unpack('<I', envelope[1:5])[0]
            if begin_key != ENVELOPE_BEGIN_KEY:
                raise ValueError("Invalid message format: Incorrect begin key.")

            # Extract the message size
            arr_size = struct.unpack('<I', envelope[5:9])[0]

            # Extract and unpack the message content
            message_data = []
            for i in range(9, 9 + arr_size, 4):
                message_data.append(struct.unpack('i', envelope[i:i + 4])[0])

            # Validate the end key and end character of the message
            end_key = struct.unpack('<I', envelope[9 + arr_size:13 + arr_size])[0]
            if end_key != ENVELOPE_END_KEY:
                raise ValueError("Invalid message format: Incorrect end key.")
            if envelope[13 + arr_size] != ENVELOPE_END_CHAR:
                raise ValueError("Invalid message format: Missing end character.")

            print("Message read successfully!")  # Print a success message
            return message_data  # Return the extracted message data

        except Exception as e:  # Handle any errors during the message reading process
            print(f"Error during read_message: {e}")
            return False  # Indicate failure in reading the message
