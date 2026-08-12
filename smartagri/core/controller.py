from smartagri.core.models import EnvironmentState, ActuatorState


class EnvironmentController:
    """
    State-aware environmental controller.

    Uses separate ON/OFF thresholds to prevent rapid
    actuator switching around a single target value.
    """

    def __init__(self, targets):
        self.targets = targets
        self.state = ActuatorState()

    def evaluate(self, environment: EnvironmentState) -> ActuatorState:
        self._control_temperature(environment.temperature)
        self._control_soil_moisture(environment.soil_moisture)
        self._control_light(environment.light)

        return ActuatorState(
            pump=self.state.pump,
            fan=self.state.fan,
            grow_light=self.state.grow_light,
        )

    def _control_temperature(self, temperature: float):
        target = self.targets["temperature"]

        if temperature > target["max"]:
            self.state.fan = True

        elif temperature < target["target"]:
            self.state.fan = False

    def _control_soil_moisture(self, moisture: float):
        target = self.targets["soil_moisture"]

        if moisture < target["min"]:
            self.state.pump = True

        elif moisture > target["target"]:
            self.state.pump = False

    def _control_light(self, light: float):
        target = self.targets["light"]

        if light < target["min"]:
            self.state.grow_light = True

        elif light > target["target"]:
            self.state.grow_light = False