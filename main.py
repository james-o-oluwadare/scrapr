# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSlot, pyqtSignal

from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel
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

# include class to read data from url and writes
#    to db, from search_engine.py

# class to read data from db and add to model
#    for display via qml listview
class DatabaseHandler(QObject):
    dataChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.model = QSqlQueryModel()
        self.model.setQuery("SELECT * FROM mytable")

    @pyqtSlot(result=QSqlQueryModel)
    def getDataModel(self):
        return self.model

    @pyqtSlot(str, str)
    def addRecord(self, name, age):
        query = QSqlQuery()
        query.prepare("INSERT INTO mytable (name, age) VALUES (?, ?)")
        query.addBindValue(name)
        query.addBindValue(age)
        query.exec_()
        self.dataChanged.emit()

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)

    # Establish the database connection
    try:
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("path/to/database.db")
        db.open()
    except:
        print("database error")

    # Create an instance of the DatabaseHandler
    databaseHandler = DatabaseHandler()

    # Load QML file
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("databaseHandler", databaseHandler)
    engine.load(os.fspath(Path(__file__).resolve().parent / "main.qml"))
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())
