from math import fmod
from datetime import timedelta


class TimeController:
    """Methods in this class round to 0, instead of flooring a
    division, as well as use the mathematic modulo (%) operation.
    This allows for negative values to return a negative time
    difference as opposed to returning 0 for negative values.
    """
    @staticmethod
    def convert_seconds(seconds):
        """Takes a number of seconds and returns the corresponding
        hours, minutes, and seconds.

        See the class description for calculation behavior.
        """
        hours = int(seconds / 3600)
        minutes = int(fmod(seconds, 3600) / 60)
        seconds = int(fmod(seconds, 60))
        return hours, minutes, seconds

    @staticmethod
    def seconds_to_string(seconds):
        hours, minutes, seconds = TimeController.convert_seconds(seconds)
        negative_str = ''
        if hours < 0 or minutes < 0 or seconds < 0:
            hours = abs(hours)
            minutes = abs(minutes)
            seconds = abs(seconds)
            negative_str = '-'
        if hours == 0:
            return f"{negative_str}{minutes}m {seconds}s"
        elif hours > 0 and minutes == 0 and seconds == 0:
            return f"{negative_str}{hours}h"
        elif hours > 0 and minutes > 0 and seconds == 0:
            return f"{negative_str}{hours}h {minutes}m"
        else:
            return f"{negative_str}{hours}h {minutes}m {seconds}s"

    @staticmethod
    def timedelta_to_string(duration):
        total_seconds = duration.total_seconds()
        return TimeController.seconds_to_string(total_seconds)
