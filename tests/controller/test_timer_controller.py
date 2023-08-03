import unittest
from datetime import datetime, timedelta

from freezegun import freeze_time

from src.controller.timer_controller import TimerController


class TestTimerController(unittest.TestCase):
    def setUp(self):
        self.dt_start = datetime(2023, 7, 18)
        self.td_session = timedelta(seconds=3728)

    def test_get_current_duration_running(self):
        with freeze_time(self.dt_start) as frozen_datetime:
            controller = TimerController()
            controller.start()

            frozen_datetime.tick(delta=self.td_session)
            self.assertEqual(controller.get_current_duration(), self.td_session)
            self.assertEqual(controller.get_current_pause_duration(), timedelta())

    def test_get_current_duration_paused(self):
        with freeze_time(self.dt_start) as frozen_datetime:
            controller = TimerController()
            controller.start()

            frozen_datetime.tick(delta=self.td_session)
            controller.pause()
            frozen_datetime.tick(delta=timedelta(seconds=70))
            self.assertEqual(controller.get_current_duration(), self.td_session)
            self.assertEqual(
                controller.get_current_pause_duration(), timedelta(seconds=70)
            )

    def test_get_current_duration_stopped(self):
        with freeze_time(self.dt_start) as frozen_datetime:
            controller = TimerController()
            controller.start()

            frozen_datetime.tick(delta=self.td_session)
            duration = controller.stop()
            self.assertEqual(duration, self.td_session)

    def test_get_current_duration_after_stopped(self):
        with freeze_time(self.dt_start) as frozen_datetime:
            controller = TimerController()
            controller.start()

            frozen_datetime.tick(delta=self.td_session)
            controller.stop()
            frozen_datetime.tick(delta=timedelta(seconds=70))
            self.assertEqual(controller.get_current_duration(), self.td_session)
            self.assertEqual(controller.get_current_pause_duration(), timedelta())

    def test_reset_from_running(self):
        with freeze_time(self.dt_start) as frozen_datetime:
            controller = TimerController()
            controller.start()

            frozen_datetime.tick(delta=self.td_session)
            controller.reset()
            self.assertEqual(controller.get_current_duration(), timedelta())
