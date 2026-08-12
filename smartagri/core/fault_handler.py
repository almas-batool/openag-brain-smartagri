from dataclasses import dataclass
from typing import Optional


@dataclass
class FaultHandlingResult:
    value: Optional[float]
    valid: bool
    used_fallback: bool
    reason: str


class SensorFaultHandler:
    """
    Converts invalid sensor readings into safe fallback values.

    The handler keeps track of the last known good reading so that
    temporary sensor failures do not immediately stop the control loop.
    """

    def __init__(self, default_value: float):
        self.default_value = default_value
        self.last_valid_value = default_value

    def handle(
        self,
        value: Optional[float],
        valid: bool,
        sensor_name: str,
    ) -> FaultHandlingResult:

        if valid and value is not None:
            self.last_valid_value = value

            return FaultHandlingResult(
                value=value,
                valid=True,
                used_fallback=False,
                reason="valid_reading",
            )

        # Sensor failure: use the most recent reliable value.
        fallback = self.last_valid_value

        return FaultHandlingResult(
            value=fallback,
            valid=False,
            used_fallback=True,
            reason=f"{sensor_name}_fallback_last_known_good",
        )