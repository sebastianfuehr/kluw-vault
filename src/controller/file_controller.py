import sqlite3

from ttkbootstrap.dialogs.dialogs import Messagebox


class FileController:
    def __init__(self, app):
        self.app = app

    def __db_backup_progress(self, status, remaining, total):
        print(f"Copied {total - remaining} of {total} pages...")

    def import_database_file(self, target_path: str):
        """Copies a database file into the local database."""
        confirmation = Messagebox.okcancel(
            parent=self.app,
            message="This will overwrite the current database! All data will be lost! Proceed?",
            title="Attention!",
        )
        if confirmation != "OK":
            print("Import operation interrupted through user input.")
            return

        self.app.session.close()
        print("Current session closed.")
        self.app.db_engine.dispose()
        print("Current engine disposed.")

        src = sqlite3.connect(target_path)
        print(f"Connected to {target_path}")
        dst = sqlite3.connect("time-journal.db")
        print("Connected to time-journal.db")
        with dst:
            src.backup(dst, pages=1, progress=self.__db_backup_progress)
            print("Backup complete")
        src.close()
        dst.close()

        # TODO: Create new session

    def export_database_file(self, target_path: str):
        """Creates a backup of the database at the indicated file path."""
        src = sqlite3.connect("time-journal.db")
        dst = sqlite3.connect(target_path)
        with dst:
            src.backup(dst, pages=1)
        src.close()
        dst.close()
