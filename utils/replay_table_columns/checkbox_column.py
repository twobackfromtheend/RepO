from typing import Union

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QCheckBox, QTableWidgetItem

from _types import GameData
from utils.replay_table_columns.base_column import BaseColumn


class CheckboxColumn(BaseColumn):
    header = "S"
    width = 1

    @classmethod
    def get_contents(cls, game_data: GameData) -> Union[QTableWidgetItem, QWidget]:
        game, path, stashed = game_data

        checkbox_cell_widget = QWidget()
        layout = QHBoxLayout(checkbox_cell_widget)
        checkbox = QCheckBox()
        checkbox.setCheckState(QtCore.Qt.Checked if stashed else QtCore.Qt.Unchecked)

        layout.addWidget(checkbox)
        layout.setAlignment(QtCore.Qt.AlignCenter)

        checkbox_cell_widget.setLayout(layout)
        return checkbox_cell_widget

