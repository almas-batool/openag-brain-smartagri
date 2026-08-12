import csv
from pathlib import Path


class SimulationAnalytics:
    """Calculates basic statistics from simulation history."""

    def __init__(self, file_path="data/simulation_log.csv"):
        self.file_path = Path(file_path)

    def load(self):
        with open(self.file_path, "r", encoding="utf-8") as file:
            return list(csv.DictReader(file))

    def summary(self):
        rows = self.load()

        if not rows:
            return {}

        def average(field):
            return sum(float(row[field]) for row in rows) / len(rows)

        return {
            "cycles": len(rows),
            "average_temperature": round(average("temperature"), 2),
            "average_humidity": round(average("humidity"), 2),
            "average_soil_moisture": round(average("soil_moisture"), 2),
            "average_light": round(average("light"), 2),
            "pump_on_cycles": sum(row["pump"] == "True" for row in rows),
            "fan_on_cycles": sum(row["fan"] == "True" for row in rows),
            "grow_light_on_cycles": sum(
                row["grow_light"] == "True" for row in rows
            ),
        }