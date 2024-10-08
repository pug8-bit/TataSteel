# Import Axis class
from quary import Axis

class AxisData:
    def __init__(self, axis, new_array):
        self.new_array = new_array  # Store the array with axis data
        self.axis = axis  # Number of available axes

    def _is_valid_axis(self, index):
        return index < self.axis and index < len(self.new_array)

    def getXaxis(self):
        if self._is_valid_axis(0): 
            axis_status = self.new_array[0][0]
            axis_position = self.new_array[0][1]
            return Axis(axis_status, axis_position)
        else:
            raise ValueError("X-axis is not available ")

    def getYaxis(self):
        if self._is_valid_axis(1):  
            axis_status = self.new_array[1][0]
            axis_position = self.new_array[1][1]
            return Axis(axis_status, axis_position)
        else:
            raise ValueError("Y-axis is not available ")

    def getZaxis(self):
        if self._is_valid_axis(2):  
            axis_status = self.new_array[2][0]
            axis_position = self.new_array[2][1]
            return Axis(axis_status, axis_position)
        else:
            raise ValueError("Z-axis is not available ")

    def getAaxis(self):
        if self._is_valid_axis(3):  
            axis_status = self.new_array[3][0]
            axis_position = self.new_array[3][1]
            return Axis(axis_status, axis_position)
        else:
            raise ValueError("A-axis is not available ")

    def getBaxis(self):
        if self._is_valid_axis(4):  
            axis_status = self.new_array[4][0]
            axis_position = self.new_array[4][1]
            return Axis(axis_status, axis_position)
        else:
            raise ValueError("B-axis is not available ")

    def getTaxis(self):
        if self._is_valid_axis(5):  
            axis_status = self.new_array[5][0]
            axis_position = self.new_array[5][1]
            return Axis(axis_status, axis_position)
        else:
            raise ValueError("T-axis is not available")

    def getRaxis(self):
        if self._is_valid_axis(6):  
            axis_status = self.new_array[6][0]
            axis_position = self.new_array[6][1]
            return Axis(axis_status, axis_position)
        else:
            raise ValueError("R-axis is not available ")