from typing import Union

from PyQt5 import QtCore
from PyQt5.QtWidgets import QTableWidgetItem, QWidget

from _types import GameData
from utils.replay_table_columns.base_column import BaseColumn
from utils.widget_utils import create_replay_table_widget_item


class ScoreColumn(BaseColumn):
    header = "Score"
    width = 10

    @classmethod
    def get_contents(cls, game_data: GameData) -> Union[QTableWidgetItem, QWidget]:
        _game = game_data[0]
        score_item = create_replay_table_widget_item(
            f"{_game.score[0]}:{_game.score[1]}",
            tooltip="\n".join([str(goal) for goal in _game.goals])
        )
        score_item.setTextAlignment(QtCore.Qt.AlignCenter)

        return score_item
