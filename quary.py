# Define the Axis class
class Axis:
    def __init__(self, axis_status, axis_position):
        self.axis_status = axis_status  # Status of the axis
        self.axis_position = axis_position  # Position of the axis (in internal units)

    def is_moving(self):
        return self.axis_status & (1 << 0) != 0
    
    def is_ready(self):
        return self.axis_status & (1 << 1) != 0
    
    def forward_limit_on(self):
        return self.axis_status & (1 << 2) != 0
    
    def reverse_limit_on(self):
        return self.axis_status & (1 << 3) != 0
    
    def is_homed(self):
        return self.axis_status & (1 << 4) != 0
    
    def is_movable_from_pc(self):
        return self.axis_status & (1 << 5) != 0
    
    def is_emergency_on(self):
        return self.axis_status & (1 << 6) != 0
    
    def get_position(self):
        return self.axis_position / 1000.0  # Convert from internal units to user-friendly units

class DeviceParameter:
    def __init__(self):
        self.AxesParameters = []  # Store AxisParameter instances

    def GetAxisParameter(self, axisIndex):
        if 0 <= axisIndex < len(self.AxesParameters):
            return self.AxesParameters[axisIndex]
        else:
            raise IndexError("Axis index out of range")

class DeviceParameter:
    def __init__(self):
        self.AxesParameters = []

    def setFromMessageArray(self, messageArray):
        # Parse axis parameters in groups of 4 (status, position, etc.)
        self.AxesParameters = []  # Reset for new data
        
        # Process the messageArray in groups of 4 parameters
        for i in range(0, len(messageArray), 4):
            axis_data = messageArray[i:i+4]  # Extract 4 elements per axis
            self.AxesParameters.append(axis_data)  # Append the axis data as a list to AxesParameters
        
     #   print(self.AxesParameters)  # Print the processed array for debugging
        return self.AxesParameters  # Return the processed list of axis parameters


