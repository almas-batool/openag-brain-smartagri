import json
import time
from dataclasses import replace
from pathlib import Path

from smartagri.simulation.sensors import VirtualEnvironment
from smartagri.simulation.actuators import VirtualActuators
from smartagri.simulation.faults import (
    FaultConfig,
    FaultType,
    SensorFaultInjector,
)
from smartagri.core.controller import EnvironmentController
from smartagri.core.safety import SafetyManager
from smartagri.core.sensor_validation import SensorValidator
from smartagri.core.fault_handler import SensorFaultHandler
from smartagri.core.data_logger import DataLogger


BASE_DIR = Path(__file__).resolve().parent


def load_crop_profile():
    path = BASE_DIR / "config" / "crops" / "tomato.json"

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def main():
    crop = load_crop_profile()
    stage = crop["stages"]["vegetative"]

    environment = VirtualEnvironment(
        temperature=30.0,
        humidity=65.0,
        soil_moisture=20.0,
        light=10000.0,
    )

    actuators = VirtualActuators()
    controller = EnvironmentController(stage)
    safety = SafetyManager()
    validator = SensorValidator()
    logger = DataLogger()

    # Sensor fault handlers
    temperature_handler = SensorFaultHandler(default_value=24.0)
    humidity_handler = SensorFaultHandler(default_value=60.0)
    soil_handler = SensorFaultHandler(default_value=50.0)
    light_handler = SensorFaultHandler(default_value=8000.0)

    # Sensor fault configuration
    temperature_fault = SensorFaultInjector(
        FaultConfig(
            fault_type=FaultType.SPIKE,
            spike_value=100.0,
        )
    )

    humidity_fault = SensorFaultInjector(
        FaultConfig(FaultType.NONE)
    )

    soil_fault = SensorFaultInjector(
        FaultConfig(FaultType.NONE)
    )

    light_fault = SensorFaultInjector(
        FaultConfig(FaultType.NONE)
    )

    print("=" * 60)
    print("SMART AGRI BRAIN - SIMULATION")
    print("=" * 60)
    print(f"Crop : {crop['name']}")
    print("Stage: vegetative")
    print()

    for cycle in range(10):

        # Apply the previous actuator state to the environment.
        environment.update(actuators.get_state())

        # Read the resulting environment.
        reading = environment.read()

        # Apply sensor faults.
        reading = replace(
            reading,
            temperature=temperature_fault.apply(
                reading.temperature
            ),
            humidity=humidity_fault.apply(
                reading.humidity
            ),
            soil_moisture=soil_fault.apply(
                reading.soil_moisture
            ),
            light=light_fault.apply(
                reading.light
            ),
        )

        # Validate sensor readings.
        temperature_check = validator.validate(
            "temperature",
            reading.temperature,
            "°C",
        )

        humidity_check = validator.validate(
            "humidity",
            reading.humidity,
            "%",
        )

        soil_check = validator.validate(
            "soil_moisture",
            reading.soil_moisture,
            "%",
        )

        light_check = validator.validate(
            "light",
            reading.light,
            "lux",
        )

        # Handle invalid readings using the last known good value.
        temperature_result = temperature_handler.handle(
            reading.temperature,
            temperature_check.valid,
            "temperature",
        )

        humidity_result = humidity_handler.handle(
            reading.humidity,
            humidity_check.valid,
            "humidity",
        )

        soil_result = soil_handler.handle(
            reading.soil_moisture,
            soil_check.valid,
            "soil_moisture",
        )

        light_result = light_handler.handle(
            reading.light,
            light_check.valid,
            "light",
        )

        # Report sensor faults.
        if not all(
            [
                temperature_check.valid,
                humidity_check.valid,
                soil_check.valid,
                light_check.valid,
            ]
        ):
            print(
                f"[{cycle + 1:02}] "
                "WARNING: Sensor fault detected - "
                "using last known good values."
            )

        # Replace invalid values with safe fallback values.
        reading = replace(
            reading,
            temperature=temperature_result.value,
            humidity=humidity_result.value,
            soil_moisture=soil_result.value,
            light=light_result.value,
        )

        # Controller decides what it wants to do.
        requested_state = controller.evaluate(reading)

        # Safety layer decides what is actually allowed.
        actuator_state = safety.validate(
            temperature=reading.temperature,
            actuator_state=requested_state,
        )

        # Apply the approved actuator state.
        actuators.set_pump(actuator_state.pump)
        actuators.set_fan(actuator_state.fan)
        actuators.set_grow_light(actuator_state.grow_light)

        state = actuators.get_state()

        logger.log(reading, state)

        print(
            f"    Temp={reading.temperature:5.2f}°C | "
            f"Humidity={reading.humidity:5.2f}% | "
            f"Soil={reading.soil_moisture:5.2f}% | "
            f"Light={reading.light:7.0f} | "
            f"Pump={'ON ' if state.pump else 'OFF'} | "
            f"Fan={'ON ' if state.fan else 'OFF'} | "
            f"Light={'ON' if state.grow_light else 'OFF'}"
        )

        time.sleep(1)


if __name__ == "__main__":
    main()