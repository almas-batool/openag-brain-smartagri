class HardwareInterface:
    """
    Hardware abstraction layer.

    Allows the control system to work with either
    simulated or real sensors/actuators.
    """

    def __init__(self, sensors, actuators):
        self.sensors = sensors
        self.actuators = actuators

    def read_environment(self):
        return self.sensors.read()

    def set_actuators(self, actuator_state):
        self.actuators.set_pump(actuator_state.pump)
        self.actuators.set_fan(actuator_state.fan)
        self.actuators.set_grow_light(actuator_state.grow_light)