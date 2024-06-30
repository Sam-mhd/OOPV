from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QTableWidget, QTableWidgetItem, QSplitter, QLabel, QSizePolicy, QMessageBox
)
from PyQt6.QtCore import Qt
import pyqtgraph as pg
import json
import numpy as np

class AnalyzeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle('Analyze App')

    def initUI(self):
        self.layout = QVBoxLayout()

        # Button to load results
        self.open_button = QPushButton('Ergebnisse laden')
        self.open_button.clicked.connect(self.load_results)
        self.layout.addWidget(self.open_button)

        # Close button
        self.close_button = QPushButton('Schließen')
        self.close_button.clicked.connect(self.confirm_close)
        self.layout.addWidget(self.close_button)

        # Table to display the results
        self.table = QTableWidget()
        self.table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.layout.addWidget(self.table)

        # Splitter to hold multiple graphs
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Histogram widget
        self.histogram_widget = pg.PlotWidget(title="Histogramm der Zeiten")
        self.histogram_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.splitter.addWidget(self.histogram_widget)

        # Average time per dataset widget
        self.avg_time_dataset_widget = pg.PlotWidget(title="Durchschnittliche Zeit pro Datensatz")
        self.avg_time_dataset_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.splitter.addWidget(self.avg_time_dataset_widget)

        # Average time per participant widget
        self.avg_time_participant_widget = pg.PlotWidget(title="Durchschnittliche Zeit pro Teilnehmer_in")
        self.avg_time_participant_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.splitter.addWidget(self.avg_time_participant_widget)

        self.layout.addWidget(self.splitter)

        self.setLayout(self.layout)

    def load_results(self):
        # Load results from a JSON file
        file_path, _ = QFileDialog.getOpenFileName(self, 'Ergebnisse laden', '', 'JSON Files (*.json)')
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    self.results = [json.loads(line) for line in f]
                self.populate_table()
                self.show_histogram()
                self.show_avg_time_per_dataset()
                self.show_avg_time_per_participant()
            except json.JSONDecodeError as e:
                self.show_error(f'Fehler beim Lesen der JSON-Datei: {e}')
            except Exception as e:
                self.show_error(f'Fehler beim Laden der Ergebnisse: {e}')

    def populate_table(self):
        # Populate the table with loaded results
        self.table.setRowCount(len(self.results))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['Teilnehmer_in', 'Zeit', 'Datensatz', 'Eintrag'])

        for row, result in enumerate(self.results):
            try:
                self.table.setItem(row, 0, QTableWidgetItem(result['Teilnehmer_in']))
                self.table.setItem(row, 1, QTableWidgetItem(str(result['Zeit'])))
                self.table.setItem(row, 2, QTableWidgetItem(result['Datensatz']))
                self.table.setItem(row, 3, QTableWidgetItem(result['Eintrag']))
            except KeyError as e:
                self.show_error(f'Fehlender Schlüssel in den Ergebnissen: {e}')

    def show_error(self, message):
        # Display an error message
        error_label = QLabel(message)
        self.layout.addWidget(error_label)

    def show_histogram(self):
        # Display a histogram of the times
        times = [result['Zeit'] for result in self.results if 'Zeit' in result]
        y, x = np.histogram(times, bins=10)
        self.histogram_widget.clear()
        self.histogram_widget.plot(x, y, stepMode=True, fillLevel=0, brush=(0, 0, 255, 150))
        self.histogram_widget.setLabel('bottom', 'Zeit (s)')
        self.histogram_widget.setLabel('left', 'Anzahl')

    def show_avg_time_per_dataset(self):
        # Display average time per dataset
        dataset_times = {}
        for result in self.results:
            dataset = result.get('Datensatz')
            if dataset:
                if dataset not in dataset_times:
                    dataset_times[dataset] = []
                dataset_times[dataset].append(result['Zeit'])

        avg_times = {dataset: sum(times) / len(times) for dataset, times in dataset_times.items()}

        x = list(avg_times.keys())
        y = list(avg_times.values())
        bg1 = pg.BarGraphItem(x=range(len(x)), height=y, width=0.6, brush='b')
        self.avg_time_dataset_widget.clear()
        self.avg_time_dataset_widget.addItem(bg1)
        self.avg_time_dataset_widget.getAxis('bottom').setTicks([list(enumerate(x))])
        self.avg_time_dataset_widget.setLabel('bottom', 'Datensatz')
        self.avg_time_dataset_widget.setLabel('left', 'Durchschnittliche Zeit (s)')

    def show_avg_time_per_participant(self):
        # Display average time per participant
        participant_times = {}
        for result in self.results:
            participant = result.get('Teilnehmer_in')
            if participant:
                if participant not in participant_times:
                    participant_times[participant] = []
                participant_times[participant].append(result['Zeit'])

        avg_times = {participant: sum(times) / len(times) for participant, times in participant_times.items()}

        x = list(avg_times.keys())
        y = list(avg_times.values())
        bg1 = pg.BarGraphItem(x=range(len(x)), height=y, width=0.6, brush='b')
        self.avg_time_participant_widget.clear()
        self.avg_time_participant_widget.addItem(bg1)
        self.avg_time_participant_widget.getAxis('bottom').setTicks([list(enumerate(x))])
        self.avg_time_participant_widget.setLabel('bottom', 'Teilnehmer_in')
        self.avg_time_participant_widget.setLabel('left', 'Durchschnittliche Zeit (s)')

    def confirm_close(self):
        # Show confirmation dialog before closing the application
        reply = QMessageBox.question(self, 'Bestätigung', 'Möchten Sie die Anwendung wirklich schließen?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.close()

if __name__ == '__main__':
    app = QApplication([])
    analyze_window = AnalyzeWindow()
    analyze_window.show()
    app.exec()
