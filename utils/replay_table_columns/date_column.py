from typing import Union

from PyQt5.QtWidgets import QTableWidgetItem, QWidget

from _types import GameData
from utils.replay_table_columns.base_column import BaseColumn
from utils.widget_utils import create_replay_table_widget_item


class DateColumn(BaseColumn):
    header = "Date"
    width = 70

    @classmethod
    def get_contents(cls, game_data: GameData) -> Union[QTableWidgetItem, QWidget]:
        return create_replay_table_widget_item(game_data[0].date.strftime("%x %X"))
