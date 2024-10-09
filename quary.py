# Define the Axis class to represent the status and position of an axis
class Axis:
    def __init__(self, axis_status, axis_position):
        self.axis_status = axis_status  # Status of the axis (bitmask of different flags)
        self.axis_position = axis_position  # Position of the axis in internal units (integer)

    # Check if the axis is currently moving (bit 0)
    def is_moving(self):
        return self.axis_status & (1 << 0) != 0
    
    # Check if the axis is ready for operation (bit 1)
    def is_ready(self):
        return self.axis_status & (1 << 1) != 0
    
    # Check if the forward limit switch is active (bit 2)
    def forward_limit_on(self):
        return self.axis_status & (1 << 2) != 0
    
    # Check if the reverse limit switch is active (bit 3)
    def reverse_limit_on(self):
        return self.axis_status & (1 << 3) != 0
    
    # Check if the axis has been homed (bit 4)
    def is_homed(self):
        return self.axis_status & (1 << 4) != 0
    
    # Check if the axis is movable from the PC (bit 5)
    def is_movable_from_pc(self):
        return self.axis_status & (1 << 5) != 0
    
    # Check if the emergency stop is active (bit 6)
    def is_emergency_on(self):
        return self.axis_status & (1 << 6) != 0
    
    # Get the position of the axis, converting from internal units to user-friendly units (e.g., millimeters)
    def get_position(self):
        return self.axis_position / 1000.0  # Conversion factor from internal units to desired units


# Define the DeviceParameter class to store and manage multiple axes parameters
class DeviceParameter:
    def __init__(self):
        self.AxesParameters = []  # List to store the parameters of multiple axes

    # Retrieve the axis parameter by index, ensuring the index is within range
    def GetAxisParameter(self, axisIndex):
        if 0 <= axisIndex < len(self.AxesParameters):
            return self.AxesParameters[axisIndex]  # Return the axis parameter at the given index
        else:
            raise IndexError("Axis index out of range")  # Raise an error if the index is invalid


# Extend the DeviceParameter class to process data from an incoming message array
class DeviceParameter:
    def __init__(self):
        self.AxesParameters = []  # List to hold axis parameter data

    # Method to parse and set axis parameters from an incoming message array
    def setFromMessageArray(self, messageArray):
        # Clear the AxesParameters list before processing new data
        self.AxesParameters = []
        
        # Loop through the message array in chunks of 4 elements (status, position, etc.)
        for i in range(0, len(messageArray), 4):
            axis_data = messageArray[i:i+4]  # Extract 4 consecutive elements for each axis
            self.AxesParameters.append(axis_data)  # Append the axis data to the AxesParameters list
        
        # Print the processed array for debugging purposes
     #   print(self.AxesParameters)
        
        # Return the list of axis parameters
        return self.AxesParameters

