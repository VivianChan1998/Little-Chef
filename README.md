# Little-Chef

# Arduino code

## Commands
upload the file `arduino/ > arduino.ino` to Arduino UNO
open the serial monitor and enter commands for testing
```
MOVE_X+1
```
moves the 2 X motors for 1 unit

```
MOVE_Y-1
```
moves the Y motors for 1 unit
```
LEDS_11_ffffff
```
on the control board, indicate that it's operating on tile (1,1).
```
LEDB_11_ffffff
```
change color of the backlighting under the little chef to `#ffffff`. (The 11 doesn't really matters in this case)

## Configuration and Calibration
- `X_STEP_ONE_BLOCK` and `Y_STEP_ONE_BLOCK`: tune this to change moving distance of motor
- `X_DIR`, `X_STEP` ...etc: the `step` and `dir` pins for each motors.
- `X_DELAY` and `Y_DELAY`: the higher the slower the motors goes.




# Python Code

- check parameters
    ```python
    IS_CONNECT = True
    # set to True when serial port is connected 
    # rpi port is always "/dev/ttyACM0", already implemented in main function

    READ_CV = True
    # set to True if testing with camera on
    # when false it uses the readily defined tiles in code
    ```

- Run `Main.py` to get started.
- close popped up windows (if any) to have it start executing on board.