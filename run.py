from pathlib import Path
from typing import List, Union

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from _types import GameData
from config import Config
from design.main_window import Ui_MainWindow
from threads import ParseReplaysThread, ToggleReplayStashThread
from utils.replay_table import populate_replays_table_view, disable_all_checkboxes, enable_all_checkboxes, \
    update_replay_table_row, stash_selection, unstash_selection, create_replays_table_columns
from utils.splash import get_splash_and_progress_bar, parse_config_with_progress_bar


class AppUi(Ui_MainWindow):
    def __init__(self, config: Config, game_datas: List[GameData]):
        self.config = config
        self.game_datas: List[GameData] = game_datas

        self.config.replay_folder_path.mkdir(exist_ok=True)
        self.config.stash_folder_path.mkdir(exist_ok=True)

        self.toggle_replay_stash_threads: List[ToggleReplayStashThread] = []

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)

        self.replays_folder_line_edit.setText(str(self.config.replay_folder_path))
        self.replays_folder_line_edit.setReadOnly(True)
        self.stash_folder_line_edit.setText(str(self.config.stash_folder_path))
        self.stash_folder_line_edit.setReadOnly(True)

        create_replays_table_columns(self.replays_table_widget)
        self.replays_table_widget.setFocusPolicy(Qt.NoFocus)
        self.replays_table_widget.verticalHeader().hide()

        self.replays_table_refresh_button.clicked.connect(self.refresh_replays)

        self.stash_button.clicked.connect(self.stash_button_clicked)
        self.unstash_button.clicked.connect(self.unstash_button_clicked)

        self.update_replay_table()

    def update_replay_table(self):
        self.replays_table_widget.setRowCount(0)

        populate_replays_table_view(self.replays_table_widget, self.game_datas, self.toggle_replay_stash)

    def refresh_replays(self):
        self.statusbar.showMessage("Refreshing replays...")
        self.replays_group_box.setDisabled(True)

        self.parse_replay_thread = ParseReplaysThread(self.config.replay_folder_path, self.config.stash_folder_path)
        self.parse_replay_thread.callback.connect(self.handle_refresh_replays_complete)
        self.parse_replay_thread.start()

    def handle_refresh_replays_complete(self, replays):
        self.game_datas = replays
        self.update_replay_table()
        self.statusbar.showMessage("Replays refreshed.", msecs=2000)
        self.replays_group_box.setDisabled(False)

    def toggle_replay_stash(self, i: int):
        disable_all_checkboxes(self.replays_table_widget)

        game, path, currently_stashed = self.game_datas[i]
        # replay_path, currently_stashed, replay_folder_path, stash_folder_path
        toggle_replay_stash_thread = ToggleReplayStashThread(path, currently_stashed, i,
                                                             self.config.replay_folder_path,
                                                             self.config.stash_folder_path)
        self.toggle_replay_stash_threads.append(toggle_replay_stash_thread)
        toggle_replay_stash_thread.callback.connect(self.handle_toggle_replay_stash_complete)
        toggle_replay_stash_thread.start()

    def handle_toggle_replay_stash_complete(self, result: Union[Exception, Path], new_stash_status: bool, i: int):
        if isinstance(result, Exception):
            print(f"Encountered exception in moving file: {result}")
        else:
            print(f"Toggle stash result: {result}")
            game_data = self.game_datas[i]
            new_game_data = game_data[0], result, new_stash_status
            self.game_datas[i] = new_game_data
            update_replay_table_row(self.replays_table_widget, i, new_game_data)
            destination_str = "stash folder" if new_stash_status else "replay folder"
            self.statusbar.showMessage(
                f"Moved replay ({new_game_data[0].name}: {new_game_data[1].name}) to {destination_str}.")
            enable_all_checkboxes(self.replays_table_widget)
        for thread in self.toggle_replay_stash_threads:
            if thread.isFinished():
                del thread

    def stash_button_clicked(self):
        stash_selection(self.replays_table_widget, self.game_datas, self.toggle_replay_stash)

    def unstash_button_clicked(self):
        unstash_selection(self.replays_table_widget, self.game_datas, self.toggle_replay_stash)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    splash, progress_bar = get_splash_and_progress_bar()
    splash.show()

    # Load game_datas and config
    config = Config()

    game_datas = parse_config_with_progress_bar(config, progress_bar, app)

    MainWindow = QtWidgets.QMainWindow()
    ui = AppUi(config, game_datas)
    ui.setupUi(MainWindow)
    MainWindow.show()

    splash.finish(MainWindow)

    sys.exit(app.exec_())
