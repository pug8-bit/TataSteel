# Project Targets Document

## Establishing a Connection with the PLC

### Purpose
To establish a communication link between the Python script and the PLC, allowing commands to be sent and responses to be received.

### Parameters
- **amc_id:** The AMS Net ID of the PLC device (e.g., `"169.254.2.227.1.1"`).
- **pyads.PORT_TC3PLC1:** The port number used for the first PLC in TwinCAT (usually `851`).

### Objective
- Create a connection using the provided **AMS Net ID** and **port number**.
- Open the connection to enable communication with the PLC.

### Return
Once the connection is established, various control and monitoring functions can be executed. A confirmation message is printed if the connection is successful. If the connection fails, an error is raised.

---

## Function Types
- **Query Functions:**
  1. `get_device_info`
  2. `get_all_parameters`

- **Command Functions:**
  1. `move_single_axis_to_location`
  2. `begin_home_operation`
  3. `stop_move`
  4. `clear_one_axis`
  5. `clear_all_axes`

---

## get_device_info(plc)

### Purpose
This function sends a request to retrieve basic information about the PLC device.

### Parameters
- **plc:** The PLC connection used to communicate with the device.

### Action Code
**500** (represented by `ACTIONCODE_GET_DEVICE_INFO` in action_code.py).

### Objective
- Send a message with the action code to retrieve device information.
- The PLC processes this request and sends the relevant information back to the PC.

### Return
- Returns **True** along with an array of device information if successful.
- The device information includes:
  1. Device ID
  2. Number of Real Axes
  3. Number of Digital Inputs (DI)
  4. Number of Digital Outputs (DO)
  5. Number of Virtual Axes
  6. Communication Port Number
  7. Diagnosis Port Number

- If the command fails or the response is invalid, **False** is returned.

---

## get_all_parameters(plc)

### Purpose
This function sends a request to retrieve all parameters associated with the device's axes, including their positions and status.

### Parameters
- **plc:** The PLC connection object used to communicate with the device.

### Action Code
**502** (represented by `ACTIONCODE_GET_ALL_PARAMETERS`).

### Objective
Send a message to the PLC using the action code `ACTIONCODE_GET_ALL_PARAMETERS` and retrieve all the parameters related to the device's axes (axis status, positions).

### Return
The function successfully returns the following:
- **True** if the parameters were successfully retrieved, along with access to:
  - Number of axes available on the device.
  - Status and position of each axis.
  
#### Accessing Axis Information
You can access the status and position of individual axes using the following methods:
- `getXaxis()`
- `getYaxis()`
- `getZaxis()`
- `getAaxis()`
- `getBaxis()`
- `getTaxis()`
- `getRaxis()`

#### Axis Information Breakdown:
Each element corresponds to a specific axis and provides the following status:
- Moving: `is_moving()`
- Ready: `is_ready()`
- Forward Limit ON: `forward_limit_on()`
- Reverse Limit ON: `reverse_limit_on()`
- Homed: `is_homed()`
- Movable from PC: `is_movable_from_pc()`
- Emergency ON: `is_emergency_on()`

#### Position of the Axis:
The current position of each axis can be accessed using `get_position()`.

- If the command fails or an invalid response is received, **False** is returned.

---

## 1. move_single_axis_to_location(plc, axisIndex, location, speed, acceleration, deceleration)

### Purpose
Moves a single axis to a specified location with the given speed, acceleration, and deceleration.

### Parameters
- **plc:** The PLC connection used for communication with the device.
- **axisIndex:** The index of the axis to be moved.
- **location:** Target location in motion units.
- **speed:** Speed of the movement.
- **acceleration:** Rate of acceleration.
- **deceleration:** Rate of deceleration.

### Action Code
**5020** (represented by `ACTIONCODE_MOVESINGLEAXIS`).

### Objective
Sends the move command to the specified axis with the defined parameters.

### Return
The function returns **True** if the move was successful, along with an array containing:
- **Warning Code:** Indicates any issues encountered during the operation.
- **Common Response:** Confirmation code from the PLC indicating the status of the command.

---

### 2. begin_home_operation(plc, axisIndex)

#### Purpose
This function sends a command to start the homing operation for a specified axis.

#### Parameters
- **plc:** The PLC connection used for communication.
- **axisIndex:** The index of the axis to be homed.

#### Action Code
**5023** (represented by `ACTIONCODE_BEGINHOMEOPERATION`).

#### Objective
The command initiates the homing sequence of the specified axis.

#### Return
- **True** if the homing operation starts successfully.
- **False** if the command fails or if there is an invalid response from the PLC.

---

### 3. stop_move(plc, axisIndex, deceleration)

#### Purpose
This function stops the movement of a single axis, decelerating at the provided rate.

#### Parameters
- **plc:** The PLC connection used for communication.
- **axisIndex:** The index of the axis to stop.
- **deceleration:** The rate at which the axis should decelerate.

#### Action Code
**5024** (represented by `ACTIONCODE_STOPMOVE`).

#### Objective
Sends a stop command to the specified axis, with controlled deceleration.

#### Return
- **True** if the stop command is successful.
- **False** if the command fails or if there is an invalid response from the PLC.

---

### 4. clear_one_axis(plc, axisIndex)

#### Purpose
This function clears the error status of a single axis, allowing it to resume normal operation.

#### Parameters
- **plc:** The PLC connection used for communication.
- **axisIndex:** The index of the axis to be cleared.

#### Action Code
**5025** (represented by `ACTIONCODE_CLEARONEAXIS`).

#### Objective
Sends a clear error command to the specified axis.

#### Return
- **True** if the error is cleared successfully.
- **False** if the command fails or if there is an invalid response from the PLC.

---

### 5. clear_all_axes(plc)

#### Purpose
This function clears the error status for all axes in the system.

#### Parameters
- **plc:** The PLC connection used for communication.

#### Action Code
**5027** (represented by `ACTIONCODE_CLEARALLAXES`).

#### Objective
Sends a clear error command for all axes at once.

#### Return
- **True** if all axis errors are cleared successfully.
- **False** if the command fails or if there is an invalid response from the PLC.



