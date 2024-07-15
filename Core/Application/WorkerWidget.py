from PyQt5.QtWidgets import QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QWidget
from Core.JSON import JSONEntityManager
from Core.Worker import UWorker
import pycountry
import re


def CheckEmail(email):
    # Регулярное выражение для проверки почтового адреса
    pattern = r'^[\w\.-]+@[a-zA-Z\d-]+\.[a-zA-Z]{2,}$'

    if re.match(pattern, email):
        return True
    else:
        return False


def GetAllCountry():
    all_countries = list(pycountry.countries)

    countries_dict = {country.name: country.alpha_2 for country in all_countries}

    countries_dict["None"] = "None"

    return countries_dict


class UErrorWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ошибка ввода email")

        self.error_label = QLabel("Неверный формат email. Пожалуйста, введите корректный email.")
        self.exit_button = QPushButton("Закрыть")
        self.exit_button.clicked.connect(self.BindClose)

        layout = QVBoxLayout()
        layout.addWidget(self.error_label)
        layout.addWidget(self.exit_button)

        self.setLayout(layout)

    def BindClose(self):
        self.close()


class UWorkerWidget(QWidget):
    def __init__(self, worker):
        super().__init__()
        self.error_window = None
        self.podrazdelenie_edit = None
        self.btn_apply = None
        self.worker = worker
        self.name_edit = None
        self.email_edit = None
        self.country_combobox = None
        self.position_combobox = None
        self.Initialization()

    def GetName(self):
        if self.worker:
            return self.worker.name
        else:
            return "No Name"

    def GetEmail(self):
        if self.worker:
            return self.worker.email
        else:
            return ""

    def GetPodrazdelenie(self):
        if self.worker:
            return self.worker.podrazdelenie
        else:
            return "None"

    def GetCountry(self):
        if self.worker:
            all_countries = GetAllCountry().items()
            small_countries = [country[1] for country in all_countries]
            big_countries = [country[0] for country in all_countries]
            return big_countries[int(small_countries.index(self.worker.country))]
        else:
            return "None"

    def GetWorkPosition(self):
        if self.worker:
            return self.worker.work_position
        else:
            return "None"

    def Initialization(self):
        if self.worker:
            self.setWindowTitle('Форма регистрации')
        else:
            self.setWindowTitle('Форма обновления')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        name_label = QLabel('Имя:')
        self.name_edit = QLineEdit()
        self.name_edit.setText(self.GetName())

        email_label = QLabel('Почта:')
        self.email_edit = QLineEdit()
        self.email_edit.setText(self.GetEmail())

        country_label = QLabel('Страна:')
        self.country_combobox = QComboBox()
        all_countries = GetAllCountry().items()
        countries = [country[0] for country in all_countries]
        self.country_combobox.addItems(countries)
        self.country_combobox.setCurrentText(self.GetCountry())

        # Создаем выпадающий список для выбора должности
        position_label = QLabel('Должность:')
        self.position_combobox = QComboBox()
        positions = JSONEntityManager.JsonApplicationLibrary.GetAllPodrazdelenieOptionNames()
        self.position_combobox.addItems(positions)
        self.position_combobox.setCurrentText(self.GetWorkPosition())

        podrazdelenie_label = QLabel('Подразделение:')
        self.podrazdelenie_edit = QLineEdit()
        self.podrazdelenie_edit.setText(self.GetPodrazdelenie())

        self.btn_apply = QPushButton('Edit')
        self.btn_apply.clicked.connect(self.BindApplySettings)

        # Добавляем виджеты на форму
        layout.addWidget(name_label)
        layout.addWidget(self.name_edit)
        layout.addWidget(email_label)
        layout.addWidget(self.email_edit)
        layout.addWidget(country_label)
        layout.addWidget(self.country_combobox)
        layout.addWidget(position_label)
        layout.addWidget(self.position_combobox)
        layout.addWidget(podrazdelenie_label)
        layout.addWidget(self.podrazdelenie_edit)
        layout.addWidget(self.btn_apply)

        self.setLayout(layout)
        self.show()

    def BindApplySettings(self):
        if not CheckEmail(self.email_edit.text()):
            self.error_window = UErrorWindow()
            self.error_window.show()
        else:
            all_countries = GetAllCountry().items()
            small_countries = [country[1] for country in all_countries]
            big_countries = [country[0] for country in all_countries]
            country = small_countries[int(big_countries.index(self.country_combobox.currentText()))]

            if self.worker:
                self.worker.name = self.name_edit.text()
                self.worker.email = self.email_edit.text()
                self.worker.country = country
                self.worker.work_position = self.position_combobox.currentText()
                self.worker.podrazdelenie = self.podrazdelenie_edit.text()
                JSONEntityManager.entity_manager.PatchWorker(self.worker)
            else:
                new_worker = UWorker()
                new_worker.name = self.name_edit.text()
                new_worker.email = self.email_edit.text()
                new_worker.country = country
                new_worker.work_position = self.position_combobox.currentText()
                new_worker.podrazdelenie = self.podrazdelenie_edit.text()
                JSONEntityManager.entity_manager.NewWorker(new_worker)
            self.close()
