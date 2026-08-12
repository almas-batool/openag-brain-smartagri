from dataclasses import dataclass
from enum import Enum
from typing import Optional
import random


class FaultType(Enum):
    """
    Types of sensor faults supported by the simulator.
    """

    NONE = "none"
    NOISE = "noise"
    STUCK = "stuck"
    SPIKE = "spike"
    MISSING = "missing"
    DRIFT = "drift"


@dataclass
class FaultConfig:
    """
    Configuration for a simulated sensor fault.
    """

    fault_type: FaultType = FaultType.NONE

    noise_range: float = 0.5
    spike_value: Optional[float] = None
    drift_per_cycle: float = 0.1
    stuck_value: Optional[float] = None


class SensorFaultInjector:
    """
    Applies controlled faults to simulated sensor readings.

    This class intentionally does not know anything about the
    controller or actuators. It only transforms sensor data.
    """

    def __init__(self, config: FaultConfig):
        self.config = config
        self._stuck_value = config.stuck_value
        self._drift_offset = 0.0

    def apply(self, value: Optional[float]) -> Optional[float]:
        """
        Apply the configured fault to a sensor value.
        """

        fault = self.config.fault_type

        if fault == FaultType.NONE:
            return value

        if fault == FaultType.NOISE:
            return self._apply_noise(value)

        if fault == FaultType.STUCK:
            return self._apply_stuck(value)

        if fault == FaultType.SPIKE:
            return self._apply_spike(value)

        if fault == FaultType.MISSING:
            return None

        if fault == FaultType.DRIFT:
            return self._apply_drift(value)

        return value

    def _apply_noise(self, value: Optional[float]) -> Optional[float]:
        if value is None:
            return None

        noise = random.uniform(
            -self.config.noise_range,
            self.config.noise_range,
        )

        return value + noise

    def _apply_stuck(self, value: Optional[float]) -> Optional[float]:
        if self._stuck_value is None:
            self._stuck_value = value

        return self._stuck_value

    def _apply_spike(self, value: Optional[float]) -> Optional[float]:
        if value is None:
            return None

        if self.config.spike_value is not None:
            return self.config.spike_value

        return value * 2

    def _apply_drift(self, value: Optional[float]) -> Optional[float]:
        if value is None:
            return None

        self._drift_offset += self.config.drift_per_cycle

        return value + self._drift_offset