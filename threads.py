from pathlib import Path

from PyQt5 import QtCore
from PyQt5.QtCore import QThread

from rrrocket_parser import parse_all_replays


class ParseReplaysThread(QThread):
    callback = QtCore.pyqtSignal(object)

    def __init__(self, replay_folder_path: Path, stash_folder_path: Path):
        super().__init__()
        self.replay_folder_path = replay_folder_path
        self.stash_folder_path = stash_folder_path

    def run(self):
        replays = [_game_data + (False,) for _game_data in parse_all_replays(self.replay_folder_path)] \
                  + [_game_data + (True,) for _game_data in parse_all_replays(self.stash_folder_path)]
        replays.sort(key=lambda _game: _game[0].date, reverse=True)

        self.callback.emit(replays)


class ToggleReplayStashThread(QThread):
    callback = QtCore.pyqtSignal(object, bool, int)  # result, new_stash_status

    def __init__(self, replay_path: Path, currently_stashed: bool, i: int, replay_folder_path: Path, stash_folder_path: Path):
        super().__init__()
        self.replay_path = replay_path
        self.currently_stashed = currently_stashed
        self.replay_folder_path = replay_folder_path
        self.stash_folder_path = stash_folder_path
        self.i = i

    def run(self):
        if self.currently_stashed:
            destination = self.replay_folder_path / self.replay_path.name
        else:
            destination = self.stash_folder_path / self.replay_path.name

        try:
            with destination.open(mode='xb') as fid:
                fid.write(self.replay_path.read_bytes())
            self.replay_path.unlink()
            self.callback.emit(destination, not self.currently_stashed, self.i)
        except FileExistsError as e:
            self.callback.emit(e, self.currently_stashed, self.i)
