The goal of this application is to provide users with a comprehensive tool for assessing real estate properties and determining their investment potential. By analyzing key financial metrics and property data, the application helps users make informed decisions about whether a property is a worthwhile investment.

It is worth noting that this application uses the output of the **'Webscraper'** application as an input.

## Application Overview

The main entry point of the application is the `run_gui.py` file. This script launches a graphical user interface (GUI) built with Tkinter. Through the GUI, users can:

- View a summary of previously analyzed properties, including relevant financial and property details.
- Input information about a new property they are interested in, such as the area, purchase price, and square meters.
- Receive calculated metrics based on their input, such as cash flow, return on investment (ROI), cap rate, and other indicators commonly used in real estate analysis.

While the application provides detailed calculations and displays the results clearly, the final decision on whether a property is a good investment remains with the user. The tool is designed to assist and inform, not to make investment decisions automatically.

## Project Structure

In addition to `run_gui.py`, the project includes several supporting Python files:

- **`clean_data.py`**: Handles data cleaning and preprocessing tasks, ensuring that property data is accurate and formatted correctly before analysis.
- **`csv_utils.py`**: Provides utility functions for reading from and writing to CSV files, enabling users to import property data or export analysis results for further review.
- **`run_analyzer.py`**: Contains the core logic for analyzing property data and calculating investment metrics. This module is used by the GUI to process user input and generate results.

Together, these components form a modular and extensible application for real estate investment analysis. Users can easily add new properties, review past analyses, and leverage the built-in calculations to support their investment decisions.