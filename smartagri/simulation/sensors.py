import random
from datetime import datetime

from smartagri.core.models import EnvironmentState


class VirtualEnvironment:
    """
    Simulates the physical growing environment.

    Environmental values change based on actuator states,
    allowing the simulator to operate as a closed-loop system.
    """

    def __init__(
        self,
        temperature=24.0,
        humidity=60.0,
        soil_moisture=50.0,
        light=8000.0,
    ):
        self.temperature = temperature
        self.humidity = humidity
        self.soil_moisture = soil_moisture
        self.light = light

    def update(self, actuators=None):
        """
        Update the simulated environment.

        Actuator effects are intentionally simplified.
        Later we can replace these with more realistic models.
        """

        # Natural environmental variation
        self.temperature += random.uniform(-0.15, 0.15)
        self.humidity += random.uniform(-0.3, 0.3)
        self.soil_moisture += random.uniform(-0.15, 0.05)
        self.light += random.uniform(-50, 50)

        if actuators:

            # Fan reduces temperature and slightly reduces humidity.
            if actuators.fan:
                self.temperature -= 0.8
                self.humidity -= 0.4

            # Pump increases soil moisture.
            if actuators.pump:
                self.soil_moisture += 2.5

            # Grow light increases simulated light intensity.
            if actuators.grow_light:
                self.light += 500

        # Keep values within physically meaningful simulation bounds.
        self.temperature = max(0.0, min(60.0, self.temperature))
        self.humidity = max(0.0, min(100.0, self.humidity))
        self.soil_moisture = max(0.0, min(100.0, self.soil_moisture))
        self.light = max(0.0, min(100000.0, self.light))

    def read(self) -> EnvironmentState:
        """
        Return the current simulated environmental state.
        """

        return EnvironmentState(
            temperature=round(self.temperature, 2),
            humidity=round(self.humidity, 2),
            soil_moisture=round(self.soil_moisture, 2),
            light=round(self.light, 2),
            timestamp=datetime.now(),
        )