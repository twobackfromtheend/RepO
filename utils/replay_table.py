from typing import Sequence, Callable, List

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QCheckBox, QTableWidget

from _types import GameData
from utils.replay_table_columns import *
from utils.widget_utils import create_replay_table_widget_item

COLUMNS = [
    CheckboxColumn,
    NameColumn,
    DateColumn,
    ScoreColumn,
    BluePlayersColumn,
    OrangePlayersColumn,
    MapColumn,
    FileNameColumn
]


def create_replays_table_columns(table: QTableWidget):
    table.setColumnCount(len(COLUMNS))

    table.setHorizontalHeaderLabels(Column.header for Column in COLUMNS)
    for i, Column in enumerate(COLUMNS):
        table.setColumnWidth(i, Column.width)


def populate_replays_table_view(table: QTableWidget, games: Sequence[GameData], toggle_replay_stash: Callable):
    for i, game_data in enumerate(games):
        game, path, stashed = game_data

        row_position = table.rowCount()
        table.insertRow(row_position)

        for column_position, Column in enumerate(COLUMNS):
            item_or_widget = Column.get_contents(game_data)
            if Column == CheckboxColumn:
                checkbox: QCheckBox = item_or_widget.findChild(QCheckBox)
                checkbox.setCheckState(QtCore.Qt.Checked if stashed else QtCore.Qt.Unchecked)
                checkbox.clicked.connect(lambda _, _i=i: table.selectRow(_i))
                checkbox.clicked.connect(lambda _, _i=i: toggle_replay_stash(_i))

            if isinstance(item_or_widget, QWidget):
                table.setCellWidget(row_position, column_position, item_or_widget)
            else:
                table.setItem(row_position, column_position, item_or_widget)


def update_replay_table_row(table: QTableWidget, row: int, game_data: GameData):
    checkbox: QCheckBox = table.cellWidget(row, 0).findChild(QCheckBox)
    checkbox.setChecked(game_data[2])

    path = game_data[1]
    filename_item = create_replay_table_widget_item(path.name, tooltip=str(path))
    table.setItem(row, table.columnCount() - 1, filename_item)


def disable_all_checkboxes(table: QTableWidget):
    rows = table.rowCount()
    for row in range(rows):
        cell_widget = table.cellWidget(row, 0)
        cell_widget.findChild(QCheckBox).setDisabled(True)


def enable_all_checkboxes(table: QTableWidget):
    rows = table.rowCount()
    for row in range(rows):
        cell_widget = table.cellWidget(row, 0)
        cell_widget.findChild(QCheckBox).setDisabled(False)


def stash_selection(table: QTableWidget, games: Sequence[GameData], toggle_replay_stash: Callable):
    selected_rows: List[int] = [selected_row.row() for selected_row in table.selectionModel().selectedRows()]

    for i in selected_rows:
        game_stashed = games[i][2]
        if not game_stashed:
            toggle_replay_stash(i)


def unstash_selection(table: QTableWidget, games: Sequence[GameData], toggle_replay_stash: Callable):
    selected_rows: List[int] = [selected_row.row() for selected_row in table.selectionModel().selectedRows()]

    for i in selected_rows:
        game_stashed = games[i][2]
        if game_stashed:
            toggle_replay_stash(i)
