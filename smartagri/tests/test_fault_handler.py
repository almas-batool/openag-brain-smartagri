from smartagri.core.fault_handler import SensorFaultHandler


def test_valid_reading_updates_last_known_value():
    handler = SensorFaultHandler(default_value=25.0)

    result = handler.handle(
        value=26.5,
        valid=True,
        sensor_name="temperature",
    )

    assert result.value == 26.5
    assert result.valid is True
    assert result.used_fallback is False


def test_invalid_reading_uses_last_known_value():
    handler = SensorFaultHandler(default_value=25.0)

    handler.handle(
        value=26.5,
        valid=True,
        sensor_name="temperature",
    )

    result = handler.handle(
        value=100.0,
        valid=False,
        sensor_name="temperature",
    )

    assert result.value == 26.5
    assert result.valid is False
    assert result.used_fallback is True


def test_first_invalid_reading_uses_default():
    handler = SensorFaultHandler(default_value=25.0)

    result = handler.handle(
        value=None,
        valid=False,
        sensor_name="temperature",
    )

    assert result.value == 25.0
    assert result.used_fallback is True