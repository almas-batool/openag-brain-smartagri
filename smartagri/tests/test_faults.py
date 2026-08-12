from smartagri.simulation.faults import (
    FaultConfig,
    FaultType,
    SensorFaultInjector,
)


def test_normal_sensor():
    injector = SensorFaultInjector(
        FaultConfig(FaultType.NONE)
    )

    assert injector.apply(25.0) == 25.0


def test_noise_sensor():
    injector = SensorFaultInjector(
        FaultConfig(
            fault_type=FaultType.NOISE,
            noise_range=1.0,
        )
    )

    value = injector.apply(25.0)

    assert 24.0 <= value <= 26.0


def test_stuck_sensor():
    injector = SensorFaultInjector(
        FaultConfig(
            fault_type=FaultType.STUCK,
        )
    )

    first = injector.apply(25.0)
    second = injector.apply(30.0)

    assert first == second


def test_spike_sensor():
    injector = SensorFaultInjector(
        FaultConfig(
            fault_type=FaultType.SPIKE,
            spike_value=100.0,
        )
    )

    assert injector.apply(25.0) == 100.0


def test_missing_sensor():
    injector = SensorFaultInjector(
        FaultConfig(
            fault_type=FaultType.MISSING,
        )
    )

    assert injector.apply(25.0) is None


def test_drifting_sensor():
    injector = SensorFaultInjector(
        FaultConfig(
            fault_type=FaultType.DRIFT,
            drift_per_cycle=1.0,
        )
    )

    first = injector.apply(25.0)
    second = injector.apply(25.0)

    assert first == 26.0
    assert second == 27.0