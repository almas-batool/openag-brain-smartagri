from smartagri.core.models import ActuatorState


class VirtualActuators:
    """
    Simulates physical actuators such as pumps, fans and grow lights.
    """

    def __init__(self):
        self.state = ActuatorState()

    def set_pump(self, enabled: bool):
        self.state.pump = enabled

    def set_fan(self, enabled: bool):
        self.state.fan = enabled

    def set_grow_light(self, enabled: bool):
        self.state.grow_light = enabled

    def get_state(self) -> ActuatorState:
        return self.state