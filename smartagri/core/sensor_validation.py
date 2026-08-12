from datetime import datetime

from smartagri.core.models import SensorReading


class SensorValidator:
    """
    Validates environmental sensor readings before
    they are passed to the control system.
    """

    RANGES = {
        "temperature": (-20.0, 60.0),
        "humidity": (0.0, 100.0),
        "soil_moisture": (0.0, 100.0),
        "light": (0.0, 100000.0),
    }

    def validate(self, sensor: str, value: float, unit: str) -> SensorReading:
        timestamp = datetime.now()

        if sensor not in self.RANGES:
            return SensorReading(
                sensor=sensor,
                value=value,
                unit=unit,
                timestamp=timestamp,
                valid=False,
                quality="unknown",
                message="Unknown sensor type.",
            )

        minimum, maximum = self.RANGES[sensor]

        if not minimum <= value <= maximum:
            return SensorReading(
                sensor=sensor,
                value=value,
                unit=unit,
                timestamp=timestamp,
                valid=False,
                quality="invalid",
                message=(
                    f"Value {value} outside allowed range "
                    f"{minimum} to {maximum}."
                ),
            )

        return SensorReading(
            sensor=sensor,
            value=value,
            unit=unit,
            timestamp=timestamp,
            valid=True,
            quality="good",
        )