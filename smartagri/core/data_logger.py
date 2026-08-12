import csv
from pathlib import Path


class DataLogger:
    """Stores simulation readings and actuator states in CSV format."""

    def __init__(self, file_path="data/simulation_log.csv"):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.file_path.exists():
            with open(self.file_path, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(
                    [
                        "timestamp",
                        "temperature",
                        "humidity",
                        "soil_moisture",
                        "light",
                        "pump",
                        "fan",
                        "grow_light",
                    ]
                )

    def log(self, reading, actuator_state):
        """Append one environment/actuator observation to the CSV log."""

        with open(self.file_path, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            writer.writerow(
                [
                    reading.timestamp.isoformat(),
                    reading.temperature,
                    reading.humidity,
                    reading.soil_moisture,
                    reading.light,
                    actuator_state.pump,
                    actuator_state.fan,
                    actuator_state.grow_light,
                ]
            )