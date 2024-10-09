import pyads
from action_code import get_device_info, get_all_parameters, move_single_axis_to_location, begin_home_operation, stop_move, clear_one_axis, clear_all_axes

# Main block to test the functions
if __name__ == "__main__":
    try:
        # AMC IP address, it connects to the automation system over network
        amc_id = "169.254.2.227.1.1"  
        plc = pyads.Connection(amc_id, pyads.PORT_TC3PLC1)  # Establish connection to the PLC
        plc.open()  # Open the PLC connection
    
        # Get and display device information
        device_info = get_device_info(plc)
        print(f"Device Info: {device_info}")

        # Retrieve all parameters of the PLC and return success status and state object
        success, state = get_all_parameters(plc)

        # Interacting with the X-axis motor state parameters
        x_axis = state.getXaxis()  # Get the X-axis from the state object
        print(f"X Axis Position: {x_axis.get_position()}")  # Get the current position of the X-axis
        print(f"X Axis Moving: {x_axis.is_moving()}")  # Check if the X-axis is currently moving
        print(f"X Axis Ready: {x_axis.is_ready()}")  # Check if the X-axis is ready for movement
        print(f"X Axis Forward Limit ON: {x_axis.forward_limit_on()}")  # Check if the forward limit is triggered
        print(f"X Axis Reverse Limit ON: {x_axis.reverse_limit_on()}")  # Check if the reverse limit is triggered
        print(f"X Axis Homed: {x_axis.is_homed()}")  # Check if the X-axis is homed
        print(f"X Axis Movable from PC: {x_axis.is_movable_from_pc()}")  # Check if the X-axis can be controlled from PC
        print(f"X Axis Emergency ON: {x_axis.is_emergency_on()}")  # Check if the emergency stop is active

        # Interacting with the Y-axis motor state parameters
        y_axis = state.getYaxis()  # Get the Y-axis from the state object
        print(f"Y Axis Position: {y_axis.get_position()}")  # Get the current position of the Y-axis
        print(f"Y Axis Ready: {y_axis.is_ready()}")  # Check if the Y-axis is ready for movement

        # Example: Move a single axis to a specific location
        axis_index = 0  # Axis index representing the X-axis (you can change it for different axes)
        move_response = move_single_axis_to_location(plc, axis_index, -10000.0, 1000.0, 1000.0, 1000.0)  
        # Move axis to -10000 units with velocity, acceleration, and deceleration set to 1000
        print(f"Move Response: {move_response}")

        # Example: Begin homing operation for a specific axis
        axis_index = 1  # Assuming 1 represents another axis, like Y-axis
        home_response = begin_home_operation(plc, axis_index)  # Start homing the Y-axis
        print(f"Home Operation Response: {home_response}")

        # Stop movement on a particular axis
        stop_response = stop_move(plc, axis_index, 10.0)  # Stop the axis within 10 units of time
        print(f"Stop Move Response: {stop_response}")

        # Clear errors or issues with one axis
        clear_axis_response = clear_one_axis(plc, axis_index)  # Clear errors for the Y-axis
        print(f"Clear One Axis Response: {clear_axis_response}")

        # Clear errors or issues for all axes
        clear_all_response = clear_all_axes(plc)  # Clear errors for all axes
        print(f"Clear All Axes Response: {clear_all_response}")

    except Exception as e:
        # Print the error if something goes wrong
        print(f"An error occurred: {e}")
    
    finally:
        # Safely close the PLC connection if it is still open
        if 'plc' in locals() and plc.is_open:
            plc.close()
            print("PLC connection closed.")
