from ttkbootstrap.toast import ToastNotification


class Notifications():

    @staticmethod
    def show_info(message, title='Info'):
        ToastNotification(
            title='Info',
            message=message,
            duration=3000
        ).show_toast()

    @staticmethod
    def show_error(message, title='Error'):
        ToastNotification(
            title='Error',
            message=message,
            duration=3000
        ).show_toast()