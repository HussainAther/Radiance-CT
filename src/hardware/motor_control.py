import time

class JanusMotorController:
    """
    Hardware Abstraction Layer (HAL) for translating RBYRCT collimator 
    decisions into physical shutter movements.
    """
    def __init__(self, port='/dev/ttyUSB0', baudrate=115200):
        self.is_connected = False
        # In Rochester, this would interface with a Stepper Motor Driver (e.g., Grbl or CAN bus)
        print(f"Initializing Janus Motor Controller on {port}...")

    def move_shutter(self, aperture_width, rotation_angle):
        """
        Translates analytical width (0.0 to 1.0) into motor steps.
        """
        # Convert 0-1.0 scale to physical millimeters/steps
        target_steps = int(aperture_width * 2000) 
        
        # This is where you would send G-Code or Serial commands:
        # e.g., self.serial.write(f"G1 X{target_steps} F500\n")
        
        print(f"[HARDWARE] Moving Shutter to {aperture_width}mm at {rotation_angle}°")
        return True

    def emergency_stop(self):
        """
        ALARA Safety Interlock: Immediately closes the shutter if dose limits are hit.
        """
        print("[ALARA] EMERGENCY STOP: Closing Janus Aperture.")
        self.move_shutter(0.0, 0.0)
