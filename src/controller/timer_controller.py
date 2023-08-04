from datetime import datetime, timedelta


class TimerController:
    def __init__(self) -> None:
        self.reset()

    def start(self) -> None:
        self.start_time = datetime.now()

    def pause(self) -> None:
        self.paused = True
        self.pause_time = datetime.now()

    def resume(self) -> timedelta:
        self.paused = False
        elapsed_time = datetime.now() - self.pause_time
        self.paused_seconds += elapsed_time.total_seconds()
        return timedelta(seconds=self.paused_seconds)

    def stop(self) -> timedelta:
        if self.paused:
            elapsed_time = datetime.now() - self.pause_time
            self.paused_seconds += elapsed_time.total_seconds()
        return self.start_time - datetime.now() - timedelta(seconds=self.paused_seconds)

    def reset(self) -> None:
        self.start_time = None
        self.pause_time = None
        self.paused_seconds = 0
        self.paused = False

    def get_current_duration(self) -> timedelta:
        if self.paused:
            curr_duration = (
                self.pause_time
                - self.start_time
                - timedelta(seconds=self.paused_seconds)
            )
        else:
            curr_duration = (
                datetime.now()
                - self.start_time
                - timedelta(seconds=self.paused_seconds)
            )
        return curr_duration

    def get_current_pause_duration(self) -> timedelta:
        return datetime.now() - self.pause_time + timedelta(seconds=self.paused_seconds)
