from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class SensorReading:
    sensor: str
    value: float
    unit: str
    timestamp: datetime
    valid: bool = True
    quality: str = "good"
    message: Optional[str] = None


@dataclass
class EnvironmentState:
    temperature: float
    humidity: float
    soil_moisture: float
    light: float
    timestamp: datetime


@dataclass
class ActuatorState:
    pump: bool = False
    fan: bool = False
    grow_light: bool = False