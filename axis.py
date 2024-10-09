# Import Axis class from the 'quary' module
from quary import Axis

# Define the AxisData class to handle data for multiple axes
class AxisData:
    def __init__(self, axis, new_array):
        self.new_array = new_array  # Store the input array containing axis data (status and position)
        self.axis = axis  # Number of available axes

    # Private method to check if the axis index is valid (i.e., within bounds of the array)
    def _is_valid_axis(self, index):
        return index < self.axis and index < len(self.new_array)  # Check both axis count and array length

    # Method to get the X-axis data (index 0)
    def getXaxis(self):
        if self._is_valid_axis(0):  # Check if the X-axis data is available
            axis_status = self.new_array[0][0]  # Get the X-axis status from the array
            axis_position = self.new_array[0][1]  # Get the X-axis position from the array
            return Axis(axis_status, axis_position)  # Return an Axis object with the status and position
        else:
            raise ValueError("X-axis is not available ")  # Raise an error if the X-axis data is not valid

    # Method to get the Y-axis data (index 1)
    def getYaxis(self):
        if self._is_valid_axis(1):  # Check if the Y-axis data is available
            axis_status = self.new_array[1][0]  # Get the Y-axis status from the array
            axis_position = self.new_array[1][1]  # Get the Y-axis position from the array
            return Axis(axis_status, axis_position)  # Return an Axis object with the status and position
        else:
            raise ValueError("Y-axis is not available ")  # Raise an error if the Y-axis data is not valid

    # Method to get the Z-axis data (index 2)
    def getZaxis(self):
        if self._is_valid_axis(2):  # Check if the Z-axis data is available
            axis_status = self.new_array[2][0]  # Get the Z-axis status from the array
            axis_position = self.new_array[2][1]  # Get the Z-axis position from the array
            return Axis(axis_status, axis_position)  # Return an Axis object with the status and position
        else:
            raise ValueError("Z-axis is not available ")  # Raise an error if the Z-axis data is not valid

    # Method to get the T-axis data (index 3)
    def getTaxis(self):
        if self._is_valid_axis(3):  # Check if the T-axis data is available
            axis_status = self.new_array[3][0]  # Get the T-axis status from the array
            axis_position = self.new_array[3][1]  # Get the T-axis position from the array
            return Axis(axis_status, axis_position)  # Return an Axis object with the status and position
        else:
            raise ValueError("T-axis is not available")  # Raise an error if the T-axis data is not valid
