<<<<<<< HEAD
Signal Analysis Project (SigAnPro v1.0)

Overview

SigAnPro v1.0 is a signal analysis tool designed to process and analyze physiological signals such as ECG and PPG. This software provides functionality to load, preprocess, and visualize signal data, with options to detect peaks, calculate heart rate, and generate various plots. The project is built using Python and PyQt for the GUI interface, making it user-friendly and accessible for users in clinical or research settings.

Features

- Signal Loading: Load ECG and PPG data from WFDB format files.
- Signal Preprocessing: Apply various filters, including bandpass, lowpass, and highpass filters.
- Peak Detection: Automatically detect R-peaks in ECG signals and P-peaks in PPG signals.
- Visualization: Generate and display plots of the signals with detected peaks.
- Customizable Parameters: Modify filtering parameters and peak detection thresholds.
- User-Friendly GUI: Easy-to-use interface with controls for all features.
- Future Possibilities: The tool has potential for further development, including advanced algorithms for cuffless blood pressure estimation, integration with wearable devices, and real-time signal processing.

Installation

To run SigAnPro v1.0, follow these steps:

1. Clone the Repository:
   ```bash
   git clone https://github.com/yourusername/SignalAnalysisProject.git
   cd SignalAnalysisProject
   ```

2. Install Dependencies:
   Make sure you have Python installed. Install the required Python packages using:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Application:
   Run the main Python script to start the application:
   ```bash
   python SigAnPro.py
   ```

4. Executable Version:
   If you want to run the standalone executable version, you can download the `.exe` file from the `dist` folder or compile it yourself using PyInstaller.

Usage

1. Load Data: Click the "Load ECG & PPG Data" button and select your data file in WFDB format.
2. Preprocess Data: Choose your filter type and click "Preprocess Data."
3. Visualize Data: Use the "Plot ECG Signal" and "Plot PPG Signal" buttons to generate and display the signal plots.
4. Save Plots: Save the generated plots using the "Save Plot" button.

Future Possibilities

- Cuffless Blood Pressure Estimation: Further algorithm development can allow for accurate cuffless blood pressure measurements.
- Real-Time Processing: Adding real-time data processing capabilities for wearable devices.
- Machine Learning Integration: Integrating machine learning models for enhanced signal interpretation and prediction.

License

This project is licensed under the MIT License. See the LICENSE file for more details.

Contact

For any inquiries or further information, feel free to contact:

Md Mohibullah 
Email: support@mdmohibullah.me
=======
# SignalAnalyzerPro_v1.0
>>>>>>> 56b88892e1bd9e819c577bbf27538e67d2116990
