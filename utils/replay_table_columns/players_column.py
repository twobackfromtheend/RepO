from typing import Union

from PyQt5.QtWidgets import QTableWidgetItem, QWidget

from _types import GameData
from utils.replay_table_columns.base_column import BaseColumn
from utils.widget_utils import create_replay_table_widget_item


class BluePlayersColumn(BaseColumn):
    header = "Blue"

    @classmethod
    def get_contents(cls, game_data: GameData) -> Union[QTableWidgetItem, QWidget]:
        return create_replay_table_widget_item(
            ", ".join(sorted(player.name for player in game_data[0].players[0])))


class OrangePlayersColumn(BaseColumn):
    header = "Orange"

    @classmethod
    def get_contents(cls, game_data: GameData) -> Union[QTableWidgetItem, QWidget]:
        return create_replay_table_widget_item(
            ", ".join(sorted(player.name for player in game_data[0].players[1])))
