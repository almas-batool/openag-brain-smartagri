from smartagri.core.models import ActuatorState


class SafetyManager:
    """
    Prevents actuator commands when environmental
    conditions are outside safe operating limits.
    """

    MAX_TEMPERATURE = 40.0
    MIN_TEMPERATURE = 5.0

    def validate(
        self,
        temperature: float,
        actuator_state: ActuatorState,
    ) -> ActuatorState:

        safe_state = ActuatorState(
            pump=actuator_state.pump,
            fan=actuator_state.fan,
            grow_light=actuator_state.grow_light,
        )

        # Extreme temperature:
        # keep ventilation active and disable irrigation.
        if temperature > self.MAX_TEMPERATURE:
            safe_state.fan = True
            safe_state.pump = False

        # Extremely low temperature:
        # disable ventilation and irrigation.
        elif temperature < self.MIN_TEMPERATURE:
            safe_state.fan = False
            safe_state.pump = False

        return safe_state