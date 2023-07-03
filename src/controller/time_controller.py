class TimeController():

    def convert_timedelta(duration):
        days, seconds = duration.days, duration.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = (seconds % 60)
        return hours, minutes, seconds

    def timedelta_to_string(duration):
        hours, minutes, seconds = TimeController.convert_timedelta(duration)
        return f'{hours}h {minutes}m {seconds}s'
