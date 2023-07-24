"""Module for the TimeController class."""

from math import fmod


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

        Examples
        --------
        >>> TimeController.convert_seconds(1)
        (0, 0, 1)
        >>> TimeController.convert_seconds(3728)
        (1, 2, 8)
        """
        hours = int(seconds / 3600)
        minutes = int(fmod(seconds, 3600) / 60)
        seconds = int(fmod(seconds, 60))
        return hours, minutes, seconds

    @staticmethod
    def seconds_to_string(seconds):
        """Converts a number of seconds into a string representation
        of hours, minutes, and seconds.

        Parameters
        ----------
        seconds : int
            The number of seconds to be converted.

        Examples
        --------
        >>> TimeController.seconds_to_string(1)
        '0m 1s'
        >>> TimeController.seconds_to_string(3600)
        '1h'
        >>> TimeController.seconds_to_string(3728)
        '1h 2m 8s'
        """
        hours, minutes, seconds = TimeController.convert_seconds(seconds)
        negative_str = ''
        if hours < 0 or minutes < 0 or seconds < 0:
            hours = abs(hours)
            minutes = abs(minutes)
            seconds = abs(seconds)
            negative_str = '-'
        if hours == 0:
            return f"{negative_str}{minutes}m {seconds}s"
        elif hours != 0 and minutes == 0 and seconds == 0:
            return f"{negative_str}{hours}h"
        elif hours != 0 and minutes != 0 and seconds == 0:
            return f"{negative_str}{hours}h {minutes}m"
        else:
            return f"{negative_str}{hours}h {minutes}m {seconds}s"

    @staticmethod
    def timedelta_to_string(duration):
        """Converts a timedelta object into a string representation
        of hours, minutes, and seconds.

        Parameters
        ----------
        duration : datetime.timedelta
            The timedelta to be converted into a string.

        Examples
        --------
        >>> TimeController.timedelta_to_string(timedelta(seconds=1))
        '0m 1s'
        >>> TimeController.timedelta_to_string(timedelta(seconds=3600))
        '1h'
        >>> TimeController.timedelta_to_string(timedelta(seconds=3728))
        '1h 2m 8s'
        """
        total_seconds = duration.total_seconds()
        return TimeController.seconds_to_string(total_seconds)
