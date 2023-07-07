class TimeController():
    @staticmethod
    def convert_seconds(seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return hours, minutes, seconds

    @staticmethod
    def convert_timedelta(duration):
        days, seconds = duration.days, duration.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return hours, minutes, seconds

    @staticmethod
    def seconds_to_string(seconds):
        hours, minutes, seconds = TimeController.convert_seconds(seconds)
        if hours == 0:
            return f'{minutes}m {seconds}s'
        elif hours > 0 and minutes == 0 and seconds == 0:
            return f'{hours}h'
        elif hours > 0 and minutes > 0 and seconds == 0:
            return f'{hours}h {minutes}m'
        else:
            return f'{hours}h {minutes}m {seconds}s'

    @staticmethod
    def timedelta_to_string(duration):
        hours, minutes, seconds = TimeController.convert_timedelta(duration)
        if hours == 0:
            return f'{minutes}m {seconds}s'
        elif hours > 0 and minutes == 0 and seconds == 0:
            return f'{hours}h'
        elif hours > 0 and minutes > 0 and seconds == 0:
            return f'{hours}h {minutes}m'
        else:
            return f'{hours}h {minutes}m {seconds}s'
