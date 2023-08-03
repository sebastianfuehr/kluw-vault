"""Tests for the TimeController component."""

from datetime import timedelta

import pytest

from src.controller.time_controller import TimeController


@pytest.mark.parametrize(
    "seconds, expected_result",
    [
        (-1, (0, 0, -1)),
        (0, (0, 0, 0)),
        (1, (0, 0, 1)),
        (60, (0, 1, 0)),
        (3600, (1, 0, 0)),
        (3728, (1, 2, 8)),
    ],
)
def test_convert_seconds(seconds, expected_result):
    """
    Parameters
    ----------
    seconds : int
        Numer of seconds to be converted into hours, minutes, and
        seconds.
    expected_result : (int, int, int)
        The expected result of the calculations as a tuple consisting
        of (hours, minutes, seconds).
    """
    assert expected_result == TimeController.convert_seconds(seconds)


@pytest.mark.parametrize(
    "seconds, expected_result",
    [
        (-1, "-0m 1s"),
        (-3600, "-1h"),
        (-3720, "-1h 2m"),
        (-3728, "-1h 2m 8s"),
        (0, "0m 0s"),
        (1, "0m 1s"),
        (60, "1m 0s"),
        (3600, "1h"),
        (3720, "1h 2m"),
        (3728, "1h 2m 8s"),
    ],
)
def test_seconds_to_string(seconds, expected_result):
    """
    Parameters
    ----------
    seconds : int
        Numer of seconds to be converted into a string.
    expected_result : str
        The expected string output.
    """
    assert expected_result == TimeController.seconds_to_string(seconds)


@pytest.mark.parametrize(
    "seconds, expected_result",
    [
        (-1, "-0m 1s"),
        (0, "0m 0s"),
        (1, "0m 1s"),
        (60, "1m 0s"),
        (3600, "1h"),
        (3720, "1h 2m"),
        (3728, "1h 2m 8s"),
    ],
)
def test_timedelta_to_string(seconds, expected_result):
    """
    Parameters
    ----------
    seconds : int
        Numer of seconds to be converted into a string.
    expected_result : str
        The expected string output.
    """
    delta = timedelta(seconds=seconds)
    assert expected_result == TimeController.timedelta_to_string(delta)
