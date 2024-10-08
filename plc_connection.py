import pyads
import struct
import time

# Constants for the message format
ENVELOPE_BEGIN_CHAR = 60  # '<' (1 byte)
ENVELOPE_BEGIN_KEY = 12345  # (4 bytes)
ENVELOPE_END_KEY = 2 * ENVELOPE_BEGIN_KEY  # (4 bytes)
ENVELOPE_END_CHAR = 62  # '>' (1 byte)
MESSAGESIZE_MAX = 2047  # 2 Kb
COMMUNICATIONSTATUS_READYFORNEWCOMMAND = 1
COMMUNICATIONSTATUS_EXECUTEDREADYFORNEWCOMMAND = 2
COMMUNICATIONSTATUS_NEWCOMMANDAVAILABLE = 3
COMMAND_STATUS_EXECUTEDREADYFORNEWCOMMAND = 4


def read_communication_status(plc):
    status = plc.read_by_name("GVL_TcpCommunication.G_wCommunicationStatus", pyads.PLCTYPE_UINT)
    return status

def wait_for_communication_status(plc):
    communication_status = read_communication_status(plc)
    return communication_status in [COMMUNICATIONSTATUS_EXECUTEDREADYFORNEWCOMMAND,COMMAND_STATUS_EXECUTEDREADYFORNEWCOMMAND]

def wait_for_communication_status_5(plc, timeout=5):
    start_time = time.time()
    while time.time() - start_time < timeout:
        communication_status = plc.read_by_name("GVL_TcpCommunication.G_wCommunicationStatus", pyads.PLCTYPE_UINT)
        if communication_status in [COMMUNICATIONSTATUS_EXECUTEDREADYFORNEWCOMMAND,COMMAND_STATUS_EXECUTEDREADYFORNEWCOMMAND]:
            return True
        read_communication_status(plc)
        time.sleep(0.05)
    return False


def send_message(plc, intArrayMessage):
    if wait_for_communication_status(plc):
        try:
            message_size = 4 * len(intArrayMessage)
            envelope = bytearray()

            # Adding begin character and key
            envelope.append(ENVELOPE_BEGIN_CHAR)
            envelope.extend(struct.pack('<I', ENVELOPE_BEGIN_KEY))

            # Adding message size
            envelope.extend(struct.pack('<I', message_size))

            # Packing the integer array into the message
            for intItem in intArrayMessage:
                envelope.extend(struct.pack('i',intItem))

            # Adding end key and character
            envelope.extend(struct.pack('<I', ENVELOPE_END_KEY))
            envelope.append(ENVELOPE_END_CHAR)

            # Writing the envelope message to the PLC memory location
            for i in range(len(envelope)):
                plc.write_by_name(f"GVL_TcpCommunication.G_aTcpReceivedArea[{i}]", envelope[i], pyads.PLCTYPE_BYTE)
            
            print("Message sent successfully!")
            plc.write_by_name("GVL_TcpCommunication.G_wCommunicationStatus", 1, pyads.PLCTYPE_DWORD)

            return True  # Indicate success

        except Exception as e:
           print(f"Error during send_message: {e}")
        return False  # Indicate failure


def read_message(plc):
    if wait_for_communication_status_5(plc):
        try:
            envelope = bytearray()

            # Reading the message bytes from PLC
            for i in range(MESSAGESIZE_MAX):
                byte = plc.read_by_name(f"GVL_TcpCommunication.G_abTcpSendArea[{i}]", pyads.PLCTYPE_BYTE)
                envelope.append(byte)

            # Validate the message format
            if envelope[0] != ENVELOPE_BEGIN_CHAR:
                raise ValueError("Invalid message format: Missing begin character.")

            # Unpack the begin key and validate
            begin_key = struct.unpack('<I', envelope[1:5])[0]
            if begin_key != ENVELOPE_BEGIN_KEY:
                raise ValueError("Invalid message format: Incorrect begin key.")

            # Unpack the message size
            arr_size = struct.unpack('<I', envelope[5:9])[0]

            # Extract message data
            message_data = []
            for i in range(9, 9 + arr_size, 4):
                message_data.append(struct.unpack('i', envelope[i:i + 4])[0])

            # Validate end key and end character
            end_key = struct.unpack('<I', envelope[9 + arr_size:13 + arr_size])[0]
            if end_key != ENVELOPE_END_KEY:
                raise ValueError("Invalid message format: Incorrect end key.")

            if envelope[13 + arr_size] != ENVELOPE_END_CHAR:
                raise ValueError("Invalid message format: Missing end character.")

            print("Message read successfully!")
            return message_data

        except Exception as e:
           print(f"Error during read_message: {e}")
           return False
