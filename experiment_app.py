from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTreeView, QColumnView,
    QLineEdit
)
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import QTimer, Qt
import json
import random
import time

class ExperimentWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        self.label = QLabel('Geben Sie Ihren Namen ein:')
        self.layout.addWidget(self.label)

        self.name_input = QLineEdit()
        self.layout.addWidget(self.name_input)

        self.start_button = QPushButton('Experiment starten')
        self.start_button.clicked.connect(self.start_experiment)
        self.layout.addWidget(self.start_button)

        self.tree_view = QTreeView()
        self.tree_view.clicked.connect(self.on_item_click)
        self.column_view = QColumnView()
        self.column_view.clicked.connect(self.on_item_click)

        self.layout.addWidget(self.tree_view)
        self.layout.addWidget(self.column_view)

        self.setLayout(self.layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.time = 0

    def start_experiment(self):
        self.name = self.name_input.text()
        if not self.name:
            self.label.setText('Bitte geben Sie Ihren Namen ein.')
            return

        self.label.setText(f'Experiment läuft für {self.name}.')
        self.start_button.setDisabled(True)

        self.current_dataset = random.choice(['data/synthetic_data.json', 'data/filesystem_data.json', 'data/biological_taxonomy.json'])
        try:
            with open(self.current_dataset, 'r') as f:
                self.data = json.load(f)
        except Exception as e:
            self.label.setText(f'Fehler beim Laden des Datensatzes: {e}')
            self.start_button.setDisabled(False)
            return

        self.search_item = random.choice(self.get_all_items(self.data))
        self.label.setText(f'Suchen Sie: {self.search_item}')

        model = self.create_model(self.data)
        self.tree_view.setModel(model)
        self.tree_view.show()
        self.column_view.hide()

        self.time = 0
        self.start_time = time.time()
        self.timer.start(1000)

    def update_timer(self):
        self.time += 1
        self.label.setText(f'Suchen Sie: {self.search_item} (Zeit: {self.time} Sekunden)')

    def get_all_items(self, data):
        items = []
        if isinstance(data, dict):
            for key, value in data.items():
                items.append(key)
                items.extend(self.get_all_items(value))
        elif isinstance(data, list):
            for value in data:
                items.extend(self.get_all_items(value))
        return items

    def create_model(self, data):
        model = QStandardItemModel()
        self.add_items(model, data)
        return model

    def add_items(self, model, data, parent=None):
        if isinstance(data, dict):
            for key, value in data.items():
                item = QStandardItem(key)
                if parent:
                    parent.appendRow(item)
                else:
                    model.appendRow(item)
                self.add_items(model, value, item)
        elif isinstance(data, list):
            for value in data:
                self.add_items(model, value, parent)
        else:
            item = QStandardItem(str(data))
            if parent:
                parent.appendRow(item)
            else:
                model.appendRow(item)

    def on_item_click(self, index):
        item = self.tree_view.model().itemFromIndex(index)
        if item.text() == self.search_item:
            self.timer.stop()
            self.time = time.time() - self.start_time
            self.label.setText(f'Gefunden! Zeit: {self.time:.2f} Sekunden')
            self.save_result()
            self.start_button.setDisabled(False)

    def save_result(self):
        result = {
            "Teilnehmer_in": self.name,
            "Zeit": self.time,
            "Datensatz": self.current_dataset,
            "Eintrag": self.search_item
        }
        try:
            with open('results.json', 'a') as f:
                json.dump(result, f)
                f.write('\n')
        except Exception as e:
            self.label.setText(f'Fehler beim Speichern der Ergebnisse: {e}')

if __name__ == '__main__':
    app = QApplication([])
    experiment_window = ExperimentWindow()
    experiment_window.show()
    app.exec()
