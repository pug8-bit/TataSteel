from plc_connection import send_message, read_message
from quary import DeviceParameter
from axis import AxisData

# Action codes for different operations
ACTIONCODE_GET_DEVICE_INFO = 500
ACTIONCODE_GET_ALL_PARAMETERS = 502
ACTIONCODE_MOVESINGLEAXIS = 5020
ACTIONCODE_BEGIN_HOME_OPERATION = 5023
ACTIONCODE_STOP_MOVE = 5024
ACTIONCODE_CLEAR_ONE_AXIS = 5025
ACTIONCODE_CLEAR_ALL_AXES = 5027

# Common response codes
COMMON_RESPONSE = 100
ACTIONSTATUS_EXECUTED = 110
ACTIONSTATUS_EXECUTEDWITHWARNING = 111
ACTIONSTATUS_NOTEXECUTED = 112
WARNING_CODE_DEFAULT = 0

# Helper function to convert values to Media Access Unit (MAU)
def ToMAU(value):
    return int(value * 1000)

# Process the read message and check for warnings
def process_read_message(readRes):
    print(readRes)
    if readRes[0] == COMMON_RESPONSE:  # Check if it's a common response
        warnCode = readRes[-1]
        if readRes[2] != ACTIONSTATUS_NOTEXECUTED:  # Check if executed successfully
            return True, readRes, warnCode
    warnCode = readRes[-1]
    return False, warnCode

# Get device info from the PLC
def get_device_info(plc):
    messageArray = [ACTIONCODE_GET_DEVICE_INFO]
    res = send_message(plc, messageArray)
    if res:
        readRes = read_message(plc)
        if readRes[0] == 501:  # Expected response code for ACTIONCODE_GET_DEVICE_INFO
            return True, readRes
    return False

# Get all parameters from the device
def get_all_parameters(plc):
    messageArray = [ACTIONCODE_GET_ALL_PARAMETERS]
    res = send_message(plc, messageArray)
    readRes = read_message(plc)

    if res:
        if readRes[0] == 503:  # Check if the response is valid
            dp = DeviceParameter()  # Create an instance of the DeviceParameter class
            new_array = dp.setFromMessageArray(readRes[5:-1])  # Process array data
            axis = readRes[3]
            status = AxisData(axis, new_array)
            return True, status  # Return the device parameters and axis status

    return False, None, None  # Return failure if the message wasn't received properly

# Move a single axis to a specific location
def move_single_axis_to_location(plc, axisIndex, location, speed, acceleration, deceleration):
    messageArray = [
        ACTIONCODE_MOVESINGLEAXIS,
        axisIndex,
        ToMAU(location),  # Convert location to MAU
        ToMAU(speed),  # Convert speed to MAU
        ToMAU(acceleration),  # Convert acceleration to MAU
        ToMAU(deceleration)  # Convert deceleration to MAU
    ]
    res = send_message(plc, messageArray)
    if res:
        readRes = read_message(plc)
        if readRes[1] == ACTIONCODE_MOVESINGLEAXIS:
            return process_read_message(readRes)
    return False

# Begin homing operation for a specific axis
def begin_home_operation(plc, axisIndex):
    messageArray = [ACTIONCODE_BEGIN_HOME_OPERATION, axisIndex]
    res = send_message(plc, messageArray)
    if res:
        readRes = read_message(plc)
        if readRes[1] == ACTIONCODE_BEGIN_HOME_OPERATION:
            return process_read_message(readRes)
    return False

# Stop the movement of a specific axis
def stop_move(plc, axisIndex, deceleration):
    messageArray = [
        ACTIONCODE_STOP_MOVE,
        axisIndex,
        ToMAU(deceleration)  # Convert deceleration to MAU
    ]
    res = send_message(plc, messageArray)
    if res:
        readRes = read_message(plc)
        if readRes[1] == ACTIONCODE_STOP_MOVE:
            return process_read_message(readRes)
    return False

# Clear alarm on one specific axis
def clear_one_axis(plc, axisIndex):
    messageArray = [ACTIONCODE_CLEAR_ONE_AXIS, axisIndex]
    res = send_message(plc, messageArray)
    if res:
        readRes = read_message(plc)
        if readRes[1] == ACTIONCODE_CLEAR_ONE_AXIS:
            return process_read_message(readRes)
    return False

# Clear alarms on all axes
def clear_all_axes(plc):
    messageArray = [ACTIONCODE_CLEAR_ALL_AXES]
    res = send_message(plc, messageArray)
    if res:
        readRes = read_message(plc)
        if readRes[1] == ACTIONCODE_CLEAR_ALL_AXES:
            return process_read_message(readRes)
    return False






