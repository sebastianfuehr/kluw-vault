from datetime import datetime, timedelta

import pytest
from freezegun import freeze_time

from src.controller.timer_controller import TimerController


@pytest.fixture
def start_date():
    return datetime(2023, 7, 18)


@pytest.fixture
def session_length():
    return timedelta(seconds=3728)


@pytest.mark.skip
def test_get_current_duration_running(start_date, session_length):
    with freeze_time(start_date) as frozen_date:
        controller = TimerController()
        controller.start()

        frozen_date.tick(delta=session_length)
        assert controller.get_current_duration() == session_length
        assert controller.get_current_pause_duration() == timedelta()


@pytest.mark.skip
def test_get_current_duration_paused(start_date, session_length):
    with freeze_time(start_date) as frozen_date:
        controller = TimerController()
        controller.start()

        frozen_date.tick(delta=session_length)
        controller.pause()
        frozen_date.tick(delta=timedelta(seconds=70))
        assert controller.get_current_duration() == session_length
        assert controller.get_current_pause_duration() == timedelta(seconds=70)


@pytest.mark.skip
def test_get_current_duration_stopped(start_date, session_length):
    with freeze_time(start_date) as frozen_date:
        controller = TimerController()
        controller.start()

        frozen_date.tick(delta=session_length)
        duration = controller.stop()
        assert duration == session_length


@pytest.mark.skip
def test_get_current_duration_after_stopped(start_date, session_length):
    with freeze_time(start_date) as frozen_date:
        controller = TimerController()
        controller.start()

        frozen_date.tick(delta=session_length)
        controller.stop()
        frozen_date.tick(delta=timedelta(seconds=70))
        assert controller.get_current_duration() == session_length
        assert controller.get_current_pause_duration() == timedelta()


@pytest.mark.skip
def test_reset_from_running(start_date, session_length):
    with freeze_time(start_date) as frozen_date:
        controller = TimerController()
        controller.start()

        frozen_date.tick(delta=session_length)
        controller.reset()
        assert controller.get_current_duration() == timedelta()
