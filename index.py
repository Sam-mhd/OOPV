import sys
import json
import time
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QTreeView, QColumnView, QLabel, QWidget, QStackedWidget, QFileDialog, QTableWidget, QTableWidgetItem, QComboBox
)
from PyQt6.QtCore import Qt, QAbstractItemModel, QModelIndex
from PyQt6.QtGui import QStandardItemModel, QStandardItem
import pyqtgraph as pg
import numpy as np

class ExperimentWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('UI Experiment and Analysis')
        self.setGeometry(100, 100, 800, 600)
        self.participant_name = ''
        self.current_dataset = ''
        self.target_entry = ''
        self.start_time = 0
        self.end_time = 0

        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Enter your name')
        self.layout.addWidget(self.name_input)

        self.topic_select = QComboBox()
        self.topic_select.addItems(['Synthetic Data', 'Real File System', 'Biological Taxonomy'])
        self.layout.addWidget(self.topic_select)

        self.start_button = QPushButton('Start Experiment')
        self.start_button.clicked.connect(self.start_experiment)
        self.layout.addWidget(self.start_button)

        self.stacked_widget = QStackedWidget()
        self.tree_view = QTreeView()
        self.column_view = QColumnView()
        self.stacked_widget.addWidget(self.tree_view)
        self.stacked_widget.addWidget(self.column_view)
        self.layout.addWidget(self.stacked_widget)

        self.target_label = QLabel('Find the following entry:')
        self.layout.addWidget(self.target_label)

        self.analysis_button = QPushButton('Go to Analysis')
        self.analysis_button.clicked.connect(self.show_analysis)
        self.layout.addWidget(self.analysis_button)

        self.central_widget.setLayout(self.layout)

    def start_experiment(self):
        self.participant_name = self.name_input.text()
        if not self.participant_name:
            print('Please enter your name.')
            return

        self.load_data()
        self.show_widget()
        self.target_label.setText(f'Find the following entry: {self.target_entry}')
        self.start_time = time.time()

    def load_data(self):
        selected_topic = self.topic_select.currentText()
        if selected_topic == 'Synthetic Data':
            self.current_dataset = 'synthetic_data'
            self.target_entry = 'target_entry'
            data = {
                'root': {
                    'child1': {
                        'target_entry': {},
                        'child1_1': {},
                    },
                    'child2': {},
                }
            }
        elif selected_topic == 'Real File System':
            self.current_dataset = 'real_file_system'
            self.target_entry = 'Documents'
            # Simulate a file system structure
            data = {
                'C:': {
                    'Program Files': {
                        'WindowsApps': {},
                        'Common Files': {},
                    },
                    'Users': {
                        'User1': {
                            'Documents': {},
                            'Pictures': {},
                        },
                        'User2': {
                            'Documents': {},
                            'Music': {},
                        }
                    },
                }
            }
        elif selected_topic == 'Biological Taxonomy':
            self.current_dataset = 'biological_taxonomy'
            self.target_entry = 'Homo sapiens'
            data = {
                'Animalia': {
                    'Chordata': {
                        'Mammalia': {
                            'Primates': {
                                'Hominidae': {
                                    'Homo': {
                                        'Homo sapiens': {},
                                    }
                                },
                                'Cebidae': {},
                            },
                            'Carnivora': {},
                        },
                        'Reptilia': {},
                    },
                }
            }
        self.populate_tree_view(data)
        self.populate_column_view(data)

    def populate_tree_view(self, data):
        model = QStandardItemModel()
        self.add_items(model, data)
        self.tree_view.setModel(model)
        self.tree_view.expandAll()

    def populate_column_view(self, data):
        model = QStandardItemModel()
        self.add_items(model, data)
        self.column_view.setModel(model)

    def add_items(self, parent, data):
        if isinstance(data, dict):
            for key, value in data.items():
                item = QStandardItem(key)
                parent.appendRow(item)
                if isinstance(value, dict):
                    self.add_items(item, value)

    def show_widget(self):
        self.stacked_widget.setCurrentIndex(0)  # Switch to tree view
        self.tree_view.clicked.connect(self.item_clicked)

        # Alternative: switch to column view
        # self.stacked_widget.setCurrentIndex(1)
        # self.column_view.clicked.connect(self.item_clicked)

    def item_clicked(self, index: QModelIndex):
        item = self.tree_view.model().itemFromIndex(index)
        if item.text() == self.target_entry:
            self.end_time = time.time()
            elapsed_time = self.end_time - self.start_time
            print(f'Time taken: {elapsed_time:.2f} seconds')
            self.save_results(elapsed_time)

    def save_results(self, elapsed_time):
        results = {
            'participant': self.participant_name,
            'dataset': self.current_dataset,
            'entry': self.target_entry,
            'time': elapsed_time
        }
        with open('results.json', 'a') as file:
            json.dump(results, file)
            file.write('\n')

    def show_analysis(self):
        self.analysis_window = AnalysisWindow()
        self.analysis_window.show()


class AnalysisWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Experiment Analysis')
        self.setGeometry(100, 100, 800, 600)
        
        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.load_button = QPushButton('Load Results')
        self.load_button.clicked.connect(self.load_results)
        self.layout.addWidget(self.load_button)

        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)

        self.plot_widget = pg.GraphicsLayoutWidget()
        self.layout.addWidget(self.plot_widget)

        self.central_widget.setLayout(self.layout)

    def load_results(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open Results File', '', 'JSON Files (*.json)')
        if file_name:
            with open(file_name, 'r') as file:
                results = [json.loads(line) for line in file]

            self.display_results(results)
            self.create_visualizations(results)

    def display_results(self, results):
        self.table_widget.setRowCount(len(results))
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(['Participant', 'Dataset', 'Entry', 'Time'])

        for row, result in enumerate(results):
            self.table_widget.setItem(row, 0, QTableWidgetItem(result['participant']))
            self.table_widget.setItem(row, 1, QTableWidgetItem(result['dataset']))
            self.table_widget.setItem(row, 2, QTableWidgetItem(result['entry']))
            self.table_widget.setItem(row, 3, QTableWidgetItem(str(result['time'])))

    def create_visualizations(self, results):
        self.plot_widget.clear()
        
        # Histogram of times
        times = [result['time'] for result in results]
        hist = pg.PlotWidget(title='Histogram of Times')
        y, x = np.histogram(times, bins='auto')
        hist.plot(x, y, stepMode=True, fillLevel=0, brush=(0,0,255,150))
        self.plot_widget.addItem(hist)

        # Bar chart of average times per dataset
        dataset_times = {}
        for result in results:
            dataset = result['dataset']
            if dataset not in dataset_times:
                dataset_times[dataset] = []
            dataset_times[dataset].append(result['time'])

        datasets = list(dataset_times.keys())
        avg_times = [sum(times)/len(times) for times in dataset_times.values()]

        bar_chart = pg.BarGraphItem(x=range(len(datasets)), height=avg_times, width=0.6, brush='r')
        bar_plot = self.plot_widget.addPlot(title='Average Times per Dataset')
        bar_plot.addItem(bar_chart)

        # Line graph of times per participant
        participants = list(set(result['participant'] for result in results))
        participant_times = {participant: [] for participant in participants}
        for result in results:
            participant_times[result['participant']].append(result['time'])

        line_plot = self.plot_widget.addPlot(title='Times per Participant')
        for participant, times in participant_times.items():
            line_plot.plot(times, pen=pg.mkPen(width=2, name=participant))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ExperimentWindow()
    window.show()
    sys.exit(app.exec())
