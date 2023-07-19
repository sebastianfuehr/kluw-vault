import unittest
from datetime import timedelta
from src.controller.time_controller import TimeController


class TestTimeController(unittest.TestCase):
    # test_convert_seconds
    def test_convert_seconds_negative(self):
        hours, minutes, seconds = TimeController.convert_seconds(-1)
        self.assertEqual(hours, 0)
        self.assertEqual(minutes, 0)
        self.assertEqual(seconds, -1)

    def test_convert_seconds_zero(self):
        hours, minutes, seconds = TimeController.convert_seconds(0)
        self.assertEqual(hours, 0)
        self.assertEqual(minutes, 0)
        self.assertEqual(seconds, 0)
    
    def test_convert_seconds_one_second(self):
        hours, minutes, seconds = TimeController.convert_seconds(1)
        self.assertEqual(hours, 0)
        self.assertEqual(minutes, 0)
        self.assertEqual(seconds, 1)

    def test_convert_seconds_one_minute(self):
        hours, minutes, seconds = TimeController.convert_seconds(60)
        self.assertEqual(hours, 0)
        self.assertEqual(minutes, 1)
        self.assertEqual(seconds, 0)
    
    def test_convert_seconds_one_hour(self):
        hours, minutes, seconds = TimeController.convert_seconds(3600)
        self.assertEqual(hours, 1)
        self.assertEqual(minutes, 0)
        self.assertEqual(seconds, 0)
    
    def test_convert_seconds_complete(self):
        hours, minutes, seconds = TimeController.convert_seconds(3728)
        self.assertEqual(hours, 1)
        self.assertEqual(minutes, 2)
        self.assertEqual(seconds, 8)

    # test_seconds_to_string
    def test_seconds_to_string_negative(self):
        res = TimeController.seconds_to_string(-1)
        self.assertEqual(res, '-0m 1s')

    def test_seconds_to_string_zero(self):
        res = TimeController.seconds_to_string(0)
        self.assertEqual(res, '0m 0s')

    def test_seconds_to_string_one_second(self):
        res = TimeController.seconds_to_string(1)
        self.assertEqual(res, '0m 1s')
    
    def test_seconds_to_string_one_minute(self):
        res = TimeController.seconds_to_string(60)
        self.assertEqual(res, '1m 0s')

    def test_seconds_to_string_one_hour(self):
        res = TimeController.seconds_to_string(3600)
        self.assertEqual(res, '1h')

    def test_seconds_to_string_even_seconds(self):
        res = TimeController.seconds_to_string(3720)
        self.assertEqual(res, '1h 2m')

    def test_seconds_to_string_complete(self):
        res = TimeController.seconds_to_string(3728)
        self.assertEqual(res, '1h 2m 8s')

    # test_timedelta_to_string
    def test_timedelta_to_string_negative(self):
        delta = timedelta(seconds=-1)
        res = TimeController.timedelta_to_string(delta)
        self.assertEqual(res, '-0m 1s')

    def test_timedelta_to_string_zero(self):
        delta = timedelta(seconds=0)
        res = TimeController.timedelta_to_string(delta)
        self.assertEqual(res, '0m 0s')

    def test_timedelta_to_string_one_second(self):
        delta = timedelta(seconds=1)
        res = TimeController.timedelta_to_string(delta)
        self.assertEqual(res, '0m 1s')
    
    def test_timedelta_to_string_one_minute(self):
        delta = timedelta(seconds=60)
        res = TimeController.timedelta_to_string(delta)
        self.assertEqual(res, '1m 0s')

    def test_timedelta_to_string_one_hour(self):
        delta = timedelta(seconds=3600)
        res = TimeController.timedelta_to_string(delta)
        self.assertEqual(res, '1h')

    def test_timedelta_to_string_even_seconds(self):
        delta = timedelta(seconds=3720)
        res = TimeController.timedelta_to_string(delta)
        self.assertEqual(res, '1h 2m')

    def test_timedelta_to_string_complete(self):
        delta = timedelta(seconds=3728)
        res = TimeController.timedelta_to_string(delta)
        self.assertEqual(res, '1h 2m 8s')

