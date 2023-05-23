# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
from PyQt5.QtCore import QAbstractListModel, Qt, QVariant, QObject, QUrl, pyqtProperty
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel, QSqlQueryModel
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine

'''
inputs:
    search term
    search site
intermediate params:
    class to search for in page
    search pattern
outputs:
    publications
internal storage:
    list result
    publications table

'''

class DatabaseModel(QAbstractListModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._data = []

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return QVariant(self._data[index.row()])
        return QVariant()

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.load(os.fspath(Path(__file__).resolve().parent / "main.qml"))
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())
