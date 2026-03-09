from fastmcp import FastMCP
import serial
import json
import time

# Initialize FastMCP server
mcp = FastMCP("Chitti")

# Constants for Chitti hardware
PORT = '/dev/ttyACM0'
BAUD = 1000000

def send_command(cmd_dict):
    try:
        with serial.Serial(PORT, BAUD, timeout=1) as ser:
            ser.write((json.dumps(cmd_dict) + "\n").encode())
            return True
    except Exception as e:
        return f"Hardware Error: {e}"

@mcp.tool()
def move_robot(direction: str, power: float = 0.2, duration: float = 0.5):
    """
    Moves Chitti. Directions: 'forward', 'backward', 'left', 'right'.
    Power: 0.0 to 1.0. Duration in seconds.
    """
    moves = {
        "forward": {"L": power, "R": power},
        "backward": {"L": -power, "R": -power},
        "left": {"L": -power, "R": power},
        "right": {"L": power, "R": -power}
    }
    
    cmd = moves.get(direction)
    if not cmd: return "Invalid direction"
    
    cmd["T"] = 1 # Motor command type
    send_command(cmd)
    time.sleep(duration)
    send_command({"T": 1, "L": 0, "R": 0}) # Stop
    return f"Chitti successfully moved {direction}."

@mcp.tool()
def get_telemetry():
    """Reads battery voltage and system status from the board."""
    try:
        with serial.Serial(PORT, BAUD, timeout=1) as ser:
            ser.write(b'{"T":131}\n')
            return ser.readline().decode().strip()
    except Exception as e:
        return f"Telemetry Error: {e}"

if __name__ == "__main__":
    mcp.run()
