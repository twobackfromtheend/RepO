from typing import Union

from PyQt5.QtWidgets import QTableWidgetItem, QWidget

from _types import GameData
from utils.replay_table_columns.base_column import BaseColumn
from utils.widget_utils import create_replay_table_widget_item


class FileNameColumn(BaseColumn):
    header = "File Name"

    @classmethod
    def get_contents(cls, game_data: GameData) -> Union[QTableWidgetItem, QWidget]:
        path = game_data[1]
        return create_replay_table_widget_item(path.name, tooltip=str(path))
