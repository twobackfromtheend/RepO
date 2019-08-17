from typing import Union

from PyQt5.QtWidgets import QTableWidgetItem, QWidget

from _types import GameData


class BaseColumn:
    header: str
    width: int = 120

    @classmethod
    def get_contents(cls, game_data: GameData) -> Union[QTableWidgetItem, QWidget]:
        raise NotImplementedError
