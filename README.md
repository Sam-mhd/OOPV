# Experiment and Analysis Program

## Motivation
User interface (UI) design isn't just about personal preferences; it's influenced by principles from cognitive science, psychology, and human-computer interaction research. Understanding these principles often requires empirical data gathered through experiments. This project aims to develop an open-source GUI application to assist in conducting such experiments.

## Scenario
Scientists want to investigate which UI components are better suited for finding specific entries within hierarchically nested structures. This involves testing two common widgets: QtTreeView, similar to Windows Explorer, and QtColumnView, akin to macOS Finder or iTunes. Participants will interact with these widgets to search through various tree structures, with their search times recorded for evaluation.

## Data Sets
To demonstrate the functionality of the program, three datasets have been prepared:

1. **Synthetic Data (`data/synthetic_data.json`)**
   - Contains randomly generated hierarchical structures composed of letters.
   - Suitable for simulating basic, artificial data scenarios.

2. **File System Data (`data/filesystem_data.json`)**
   - Represents a real-world application scenario.
   - Mimics a hierarchical structure similar to that of a file system.

3. **Biological Taxonomy (`data/biological_taxonomy.json`)**
   - Represents a taxonomy structure commonly found in biology, media, or library sciences.
   - Demonstrates a complex hierarchical data structure.

Each dataset includes predefined entries that participants will search for during the experiment. These datasets are stored as JSON files for easy handling using the `json` or `orjson` packages.

## Development Requirements

### Libraries and Tools
- **Python**: Version 3.6 or higher.
- **PyQt6**: Python bindings for Qt, used for building the GUI application.
  - Install using `pip install PyQt6`.
- **pyqtgraph**: Scientific graphics and GUI library for PyQt.
  - Install using `pip install pyqtgraph`.
- **numpy**: Fundamental package for scientific computing with Python.
  - Install using `pip install numpy`.

### Development Environment
- **IDE**: Any Python-compatible integrated development environment (IDE) like PyCharm, Visual Studio Code, or Jupyter Notebook.
 
## Workflow
1. **Experiment Interface (`experiment_app.py`)**
   - Participants start by entering their name.
   - They initiate an experiment session by clicking a button.
   - A timer starts, and one of the two widgets (chosen randomly) displays the hierarchical structure alongside the entry they need to find.
   - Once found, the timer stops, and results (participant name, time taken, dataset, and entry) are recorded.
   - Participants can start another experiment session without re-entering their name or exit the application.

2. **Analysis Interface (`analyze_app.py`)**
   - Scientists can load experiment results from JSON files.
   - Results are displayed in a table format (columns: Participant, Time, Dataset, Entry).
   - Additionally, three visualizations using `pyqtgraph` are generated:
     - Histogram of search times to understand distribution.
     - Bar graph showing average search times per dataset to compare performance.
     - Bar graph displaying average search times per participant to analyze individual performance.

## Conclusion
This project aims to provide a user-friendly GUI application for conducting UI experimentations, backed by empirical data. It facilitates understanding of how different UI components perform in searching hierarchical structures, potentially informing future UI design decisions based on scientific findings.
