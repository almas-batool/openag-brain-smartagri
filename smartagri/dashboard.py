import csv
from pathlib import Path


LOG_FILE = Path("data/simulation_log.csv")


def load_data():
    if not LOG_FILE.exists():
        return []

    with open(LOG_FILE, "r", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def main():
    rows = load_data()

    print("=" * 60)
    print("SMART AGRI BRAIN - DASHBOARD")
    print("=" * 60)

    if not rows:
        print("No simulation data available.")
        return

    latest = rows[-1]

    print("\nCURRENT ENVIRONMENT")
    print(f"Temperature   : {latest['temperature']} °C")
    print(f"Humidity      : {latest['humidity']} %")
    print(f"Soil moisture : {latest['soil_moisture']} %")
    print(f"Light         : {latest['light']} lux")

    print("\nACTUATORS")
    print(f"Pump          : {'ON' if latest['pump'] == 'True' else 'OFF'}")
    print(f"Fan           : {'ON' if latest['fan'] == 'True' else 'OFF'}")
    print(
        f"Grow light    : "
        f"{'ON' if latest['grow_light'] == 'True' else 'OFF'}"
    )

    print("\nSYSTEM")
    print(f"Cycles logged : {len(rows)}")
    print(f"Last update   : {latest['timestamp']}")

    print("=" * 60)


if __name__ == "__main__":
    main()