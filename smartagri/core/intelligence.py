class CropIntelligence:
    """
    Provides simple rule-based crop recommendations.

    This layer analyzes the current environment against
    the crop growth-stage targets.
    """

    def __init__(self, stage):
        self.stage = stage

    def analyze(self, reading):
        recommendations = []

        self._check(
            recommendations,
            "temperature",
            reading.temperature,
        )

        self._check(
            recommendations,
            "humidity",
            reading.humidity,
        )

        self._check(
            recommendations,
            "soil_moisture",
            reading.soil_moisture,
        )

        self._check(
            recommendations,
            "light",
            reading.light,
        )

        if not recommendations:
            recommendations.append(
                "All environmental conditions are within the target range."
            )

        return recommendations

    def _check(self, recommendations, name, value):
        limits = self.stage[name]

        if value < limits["min"]:
            recommendations.append(
                f"{name}: below target - increase toward "
                f"{limits['target']}."
            )

        elif value > limits["max"]:
            recommendations.append(
                f"{name}: above target - reduce toward "
                f"{limits['target']}."
            )