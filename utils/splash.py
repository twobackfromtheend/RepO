from typing import Tuple

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt

from config import Config
from game import Game
from rrrocket_parser import parse_replay


def get_splash_and_progress_bar() -> Tuple[QtWidgets.QSplashScreen, QtWidgets.QProgressBar]:
    # Splash
    splash_pix = QtGui.QPixmap('calculated_logo_flair_resized.png')

    splash = QtWidgets.QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
    splash.setEnabled(False)

    progress_bar = QtWidgets.QProgressBar(splash)
    progress_bar.setGeometry(0, splash_pix.height() - 50, splash_pix.width(), 25)
    progress_bar.setStyleSheet(
        """
        QProgressBar {
            border: 1px solid black;
            height: 500px;
            text-align: center;
            padding: 1px;
            border-radius: 7px;
            background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #fff,
                stop: 0.4999 #eee,
                stop: 0.5 #ddd,
                stop: 1 #eee 
            );
            width: 15px;
        }
        
        QProgressBar::chunk {
            background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #7df,
                stop: 0.4999 #7bd,
                stop: 0.5 #49b,
                stop: 1 #48a 
            );
            border-radius: 7px;
            border: 1px solid black;
        }
        """
    )
    progress_bar_palette = QtGui.QPalette()
    progress_bar_palette.setColor(QtGui.QPalette.Text, QtGui.QColor("black"))
    progress_bar.setPalette(progress_bar_palette)
    return splash, progress_bar


def parse_config_with_progress_bar(config: Config, progress_bar, app: QtWidgets.QApplication):
    unstashed_replay_paths = list(config.replay_folder_path.glob("*.replay"))
    stashed_replay_paths = list(config.stash_folder_path.glob("*.replay"))
    unstashed_replay_paths_count = len(unstashed_replay_paths)
    stashed_replay_paths_count = len(stashed_replay_paths)
    print(f"Found {unstashed_replay_paths_count} unstashed replays, {stashed_replay_paths_count} stashed replays.")

    progress_bar.setMaximum(unstashed_replay_paths_count + stashed_replay_paths_count)
    parsed_count = 0
    game_datas = []
    for replay_path in unstashed_replay_paths:
        _game_data = Game(parse_replay(replay_path)['properties'])
        game_datas.append((_game_data, replay_path, False))
        parsed_count += 1
        progress_bar.setValue(parsed_count)
        app.processEvents()
    for replay_path in stashed_replay_paths:
        _game_data = Game(parse_replay(replay_path)['properties'])
        game_datas.append((_game_data, replay_path, True))
        parsed_count += 1
        progress_bar.setValue(parsed_count)
        app.processEvents()

    game_datas.sort(key=lambda _game: _game[0].date, reverse=True)
    return game_datas
