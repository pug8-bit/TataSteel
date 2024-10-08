import pyads
from action_code import get_device_info,get_all_parameters,move_single_axis_to_location,begin_home_operation,stop_move,clear_one_axis,clear_all_axes

# Main block to test the functions
if __name__ == "__main__":
    try:
        amc_id = "169.254.2.227.1.1"  
        plc = pyads.Connection(amc_id, pyads.PORT_TC3PLC1)
        plc.open()
    
        device_info = get_device_info(plc)
        print(f"Device Info: {device_info}")

        success,state = get_all_parameters(plc)

        # Example of using individual axes
        x_axis = state.getXaxis()
        print(f"X Axis Position: {x_axis.get_position()}")
        print(f"X Axis Moving: {x_axis.is_moving()}")
        print(f"Y Axis Ready: {x_axis.is_ready()}")
        print(f"X Axis Forward Limit ON: {x_axis.forward_limit_on()}")
        print(f"X Axis Reverse Limit ON: {x_axis.reverse_limit_on()}")       
        print(f"X Axis Homed: {x_axis.is_homed()}")        
        print(f"X Axis Movable from PC: {x_axis.is_movable_from_pc()}")        
        print(f"X Axis Emergency ON: {x_axis.is_emergency_on()}")

        y_axis = state.getYaxis()
        print(f"Y Axis Position: {y_axis.get_position()}")
        print(f"Y Axis Ready: {y_axis.is_ready()}")


        axis_index = 0  

        move_response = move_single_axis_to_location(plc, axis_index, -10000.0, 1000.0, 1000.0, 1000.0)
        print(f"Move Response: {move_response}")
        axis_index = 1  # Example index
        home_response = begin_home_operation(plc, axis_index)
        print(f"Home Operation Response: {home_response}")

        # Test stopping move
        stop_response = stop_move(plc, axis_index, 10.0)
        print(f"Stop Move Response: {stop_response}")

        # Test clearing one axis
        clear_axis_response = clear_one_axis(plc, axis_index)
        print(f"Clear One Axis Response: {clear_axis_response}")

        # Test clearing all axes
        clear_all_response = clear_all_axes(plc)
        print(f"Clear All Axes Response: {clear_all_response}")

    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
    
        if 'plc' in locals() and plc.is_open:
            plc.close()
            print("PLC connection closed.")

