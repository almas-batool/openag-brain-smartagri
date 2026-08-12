from smartagri.core.analytics import SimulationAnalytics


def main():
    analytics = SimulationAnalytics()
    summary = analytics.summary()

    print("=" * 50)
    print("SMART AGRI BRAIN - ANALYTICS")
    print("=" * 50)

    if not summary:
        print("No simulation data available.")
        return

    print(f"Cycles recorded       : {summary['cycles']}")
    print(f"Average temperature   : {summary['average_temperature']} °C")
    print(f"Average humidity      : {summary['average_humidity']} %")
    print(f"Average soil moisture : {summary['average_soil_moisture']} %")
    print(f"Average light         : {summary['average_light']} lux")
    print(f"Pump ON cycles        : {summary['pump_on_cycles']}")
    print(f"Fan ON cycles         : {summary['fan_on_cycles']}")
    print(f"Grow light ON cycles  : {summary['grow_light_on_cycles']}")


if __name__ == "__main__":
    main()