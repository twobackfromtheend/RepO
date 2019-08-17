from PyQt5 import QtCore
from PyQt5.QtWidgets import QTableWidgetItem


def create_replay_table_widget_item(text: str, editable: bool = False, tooltip: str = None):
    item = QTableWidgetItem(text)

    if tooltip is None:
        item.setToolTip(text)
    else:
        item.setToolTip(tooltip)
    if not editable:
        item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
    return item