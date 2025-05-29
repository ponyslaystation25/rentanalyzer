import sys
import run_analyzer
from PyQt5.QtWidgets import QGroupBox, QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QScrollArea, QHBoxLayout
from PyQt5.QtCore import Qt

def dataframe_to_table(df, width, height):
    # Create a table widget
    table = QTableWidget()
    table.setRowCount(df.shape[0])
    table.setColumnCount(df.shape[1])
    table.setHorizontalHeaderLabels(df.columns)

    # Fill the table with DataFrame values
    for i in range(df.shape[0]):
        for j in range(df.shape[1]):
            value = str(df.iloc[i, j])
            table.setItem(i, j, QTableWidgetItem(value))
    table.resizeColumnsToContents()
    table.setFixedSize(width, height)
    return table

def main():
    # Analyze the data
    df, rent_per_m2_stats = run_analyzer.analyze()
    # Get the top 15 properties by *
    # Prepare tables for the GUI
    tables = [
        ("Top 15 Properties by Mean Rent per m2", run_analyzer.top_15_mean_rent_per_m2(rent_per_m2_stats)),
        ("Top 15 Properties by Maximum Rent per m2", run_analyzer.top_15_rent_per_m2(rent_per_m2_stats)),
        ("Lowest 15 Properties by Mean Rent per m2", run_analyzer.low_15_mean_rent_per_m2(rent_per_m2_stats)),
        ("Lowest 15 Properties by Minimum Rent per m2", run_analyzer.low_15_min_rent_per_m2(rent_per_m2_stats)),
        ("Top 15 Properties by Standard Deviation in rent per m2", run_analyzer.top_15_stddev_rent_per_m2(rent_per_m2_stats)),
        ("Lowest 15 Properties by Standard Deviation in rent per m2", run_analyzer.low_15_stddev_rent_per_m2(rent_per_m2_stats))
    ]

    # Create the main application window
    # Create the application and main window
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    main_window.setWindowTitle("Property Analyzer")


    # Set the main layout
    # Create the different Groupboxes
    left_group = QGroupBox("User Input")
    left_layout = QVBoxLayout()
    # Placeholder for user input widgets
    left_layout.addWidget(QLabel("User input widgets will go here."))
    left_layout.addStretch(1)  # Add stretch to push content to the top
    left_group.setLayout(left_layout)

    # Create the right group box for analysis results
    right_group = QGroupBox("Analysis Results")
    tables_layout = QVBoxLayout()
    # Loop through the tables and add them to the layout
    for label_text, table_df in tables:
        # Create a label for the table
        pair_layout = QVBoxLayout()
        label = QLabel(label_text)
        label.setAlignment(Qt.AlignHCenter)
        label.setStyleSheet("font-size: 20px; font-weight: bold;")
        pair_layout.addWidget(label)
        # Convert the DataFrame to a table widget
        table_widget = dataframe_to_table(table_df, 750, 500)
        pair_layout.addWidget(table_widget)
        tables_layout.addLayout(pair_layout)


    # Connect the button and connect to the quit function
    button = QPushButton("Quit Application")
    button.clicked.connect(app.quit)
    tables_layout.addWidget(button)
    right_group.setLayout(tables_layout)

    # Create a scroll area for the right group
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setWidget(right_group)  # Set the right group as the scrollable widget

    # Create a horizontal layout to hold the tables and add a stretchable spacer
    main_layout = QHBoxLayout()
    main_layout.addWidget(left_group, 1)  # Add the left group with stretch factor 1
    main_layout.addWidget(scroll, 1)  # Add the right group with stretch factor 3 right box is wider
    
    # Create a container widget to hold the main layout
    container = QWidget()
    container.setLayout(main_layout)
    main_window.setCentralWidget(container)

    # Set the minimum size of the main window
    main_window.setMinimumSize(1500, 1000)
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
