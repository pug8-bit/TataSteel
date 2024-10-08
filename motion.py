import time
from action_code import  get_all_parameters

def monitor_axes(plc):
    while True:
        try:
            success, readRes, axis_status_descriptions = get_all_parameters(plc)

            if success:
                for axis_desc in axis_status_descriptions:
                    axis_index, status_descriptions, position = axis_desc
                    print(f"{axis_index}: Status - {', '.join(status_descriptions)}, Position - {position:.2f}")

            else:
                print("Failed to retrieve parameters.")

            time.sleep(0.001)  

        except Exception as e:
            print(f"An error occurred: {e}")
            break
