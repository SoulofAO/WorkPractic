import sys

from PyQt5 import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, \
    QAbstractItemView, QLabel, QLineEdit, QComboBox
from Core.JSON import JSONEntityManager
import pycountry
from Core.Application import WorkerWidget
import re


def GetAllCountry():
    all_countries = list(pycountry.countries)

    countries_dict = {country.name: country.alpha_2 for country in all_countries}

    countries_dict["None"] = "None"

    return countries_dict


class UMainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.entity_manager = JSONEntityManager.entity_manager
        self.entity_manager.new_worker_delegate.AddHandler(self.BindNewWorker)
        self.entity_manager.remove_worker_delegate.AddHandler(self.BindRemoveWorker)
        self.entity_list = None
        self.btn_new = None
        self.btn_delete = None
        self.btn_edit = None
        self.worker_widget = None
        self.workers = []
        self.Initialization()

    def BindNewWorker(self, worker):
        self.workers.append(worker)
        self.entity_list.addItem(worker.name)

    def BindRemoveWorker(self, worker):
        index = self.workers.index(worker)
        self.workers.remove(worker)
        self.entity_list.takeItem(index)

    def Initialization(self):
        self.setWindowTitle('Управление сущностями')
        self.setGeometry(100, 100, 400, 300)

        layout = QHBoxLayout()

        # Создаем список сущностей
        self.entity_list = QListWidget()
        self.entity_list.setSelectionMode(QAbstractItemView.SingleSelection)
        entities = []
        self.workers = self.entity_manager.workers.copy()
        for worker in self.entity_manager.workers:
            entities.append(worker.name)
        self.entity_list.addItems(entities)

        # Создаем кнопки
        self.btn_new = QPushButton('New')
        self.btn_delete = QPushButton('Delete')
        self.btn_edit = QPushButton('Edit')
        self.btn_new.clicked.connect(self.BindClickOnNewWorker)
        self.btn_edit.clicked.connect(self.BindClickOnEditWorker)
        self.btn_delete.clicked.connect(self.BindClickOnRemoveWorker)

        # Добавляем виджеты на форму
        layout.addWidget(self.entity_list)
        layout_buttons = QVBoxLayout()
        layout_buttons.addWidget(self.btn_new)
        layout_buttons.addWidget(self.btn_delete)
        layout_buttons.addWidget(self.btn_edit)
        layout.addLayout(layout_buttons)

        self.setLayout(layout)
        self.show()

    def BindClickOnNewWorker(self):
        self.worker_widget = WorkerWidget.UWorkerWidget(None)

    def BindClickOnEditWorker(self):
        selected_index = self.entity_list.currentRow()
        worker = self.workers[selected_index]
        self.worker_widget = WorkerWidget.UWorkerWidget(worker)

    def BindClickOnRemoveWorker(self):
        selected_index = self.entity_list.currentRow()
        worker = self.workers[selected_index]
        self.entity_manager.DeleteWorker(worker)


