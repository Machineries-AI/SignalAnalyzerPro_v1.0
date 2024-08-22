import sys
import wfdb
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QFileDialog, QComboBox
from scipy.signal import butter, filtfilt, find_peaks, welch

class SignalAnalyzer(QWidget):
    def __init__(self):
        super().__init__()
        self.ecg_signal = None
        self.ppg_signal = None
        self.filtered_ecg_signal = None
        self.filtered_ppg_signal = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Signal Analyzer')
        self.setGeometry(100, 100, 200, 300)
        layout = QVBoxLayout()

        # Status Label
        self.status_label = QLabel('Status: Ready')
        layout.addWidget(self.status_label)

        # Sample Numbers
        self.sample_label = QLabel('Sample Numbers (start, end):')
        self.sample_input = QLineEdit('10000, 20000')  # Default values
        layout.addWidget(self.sample_label)
        layout.addWidget(self.sample_input)
        
        # Height and Distance
        self.height_label = QLabel('Height Threshold:')
        self.height_input = QLineEdit('500')
        layout.addWidget(self.height_label)
        layout.addWidget(self.height_input)
        
        self.distance_label = QLabel('Distance Threshold:')
        self.distance_input = QLineEdit('250')
        layout.addWidget(self.distance_label)
        layout.addWidget(self.distance_input)
        
        # Filter Options
        self.filter_label = QLabel('Filter Type:')
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(['Bandpass (0.5-40 Hz)', 'Lowpass (40 Hz)', 'Highpass (0.5 Hz)'])
        layout.addWidget(self.filter_label)
        layout.addWidget(self.filter_combo)
        
        # Load Data Button
        self.load_button = QPushButton('Load ECG & PPG Data')
        self.load_button.clicked.connect(self.load_data)
        layout.addWidget(self.load_button)
        
        # Preprocess Data Button
        self.preprocess_button = QPushButton('Preprocess Data')
        self.preprocess_button.clicked.connect(self.preprocess_data)
        layout.addWidget(self.preprocess_button)
        
        # Plot Buttons
        self.plot_button = QPushButton('Plot ECG Signal')
        self.plot_button.clicked.connect(self.plot_signal)
        layout.addWidget(self.plot_button)
        
        self.plot_ppg_button = QPushButton('Plot PPG Signal')
        self.plot_ppg_button.clicked.connect(self.plot_ppg_signal)
        layout.addWidget(self.plot_ppg_button)
        
        self.plot_psd_button = QPushButton('Plot PSD (ECG)')
        self.plot_psd_button.clicked.connect(self.plot_psd)
        layout.addWidget(self.plot_psd_button)
        
        # Save Plot Button
        self.save_button = QPushButton('Save Plot')
        self.save_button.clicked.connect(self.save_plot)
        layout.addWidget(self.save_button)

        # Copyright Statement
        self.copyright_label = QLabel('© 2024 MD Mohibullah. All rights reserved.')
        layout.addWidget(self.copyright_label)
        
        self.setLayout(layout)

    def load_data(self):
        file_dialog = QFileDialog()
        file_name, _ = file_dialog.getOpenFileName(self, "Open Data", "", "WFDB Files (*.dat);;All Files (*)")
        if file_name:
            self.data_file = file_name
            record = wfdb.rdrecord(self.data_file.replace('.dat', ''))
            self.ecg_signal = record.p_signal[:, 0]  # Assuming ECG is the first channel
            self.ppg_signal = record.p_signal[:, 1]  # Assuming PPG is the second channel
            
            # Check for NaN values in the raw PPG signal
            if np.isnan(self.ppg_signal).any():
                print("NaN values detected in the raw PPG signal.")
            else:
                print("No NaN values in the raw PPG signal.")
            
            self.status_label.setText("Status: Data loaded successfully!")
        else:
            self.status_label.setText("Status: Failed to load data.")

    def preprocess_data(self):
        if self.ecg_signal is None or self.ppg_signal is None:
            self.status_label.setText("Status: No data loaded.")
            return
        
        # Handle NaN values in the PPG signal
        if np.isnan(self.ppg_signal).any():
            self.ppg_signal = np.nan_to_num(self.ppg_signal)  # Replace NaN with zero (or use interpolation if needed)
            print("Replaced NaN values in the PPG signal.")
        
        filter_type = self.filter_combo.currentText()
        if filter_type == 'Bandpass (0.5-40 Hz)':
            self.filtered_ecg_signal = self.bandpass_filter(self.ecg_signal)
            self.filtered_ppg_signal = self.bandpass_filter(self.ppg_signal)
        elif filter_type == 'Lowpass (40 Hz)':
            self.filtered_ecg_signal = self.lowpass_filter(self.ecg_signal)
            self.filtered_ppg_signal = self.lowpass_filter(self.ppg_signal)
        elif filter_type == 'Highpass (0.5 Hz)':
            self.filtered_ecg_signal = self.highpass_filter(self.ecg_signal)
            self.filtered_ppg_signal = self.highpass_filter(self.ppg_signal)
        
        print(f'First few values of filtered PPG signal: {self.filtered_ppg_signal[:10]}')  # Debugging statement
        self.status_label.setText("Status: Data preprocessed successfully!")

    def bandpass_filter(self, signal, lowcut=0.5, highcut=40.0, fs=256.0, order=4):
        nyquist = 0.5 * fs
        low = lowcut / nyquist
        high = highcut / nyquist
        b, a = butter(order, [low, high], btype='band')
        return filtfilt(b, a, signal)

    def lowpass_filter(self, signal, highcut=40.0, fs=256.0, order=4):
        nyquist = 0.5 * fs
        high = highcut / nyquist
        b, a = butter(order, high, btype='low')
        return filtfilt(b, a, signal)

    def highpass_filter(self, signal, lowcut=0.5, fs=256.0, order=4):
        nyquist = 0.5 * fs
        low = lowcut / nyquist
        b, a = butter(order, low, btype='high')
        return filtfilt(b, a, signal)

    def plot_signal(self):
        if self.filtered_ecg_signal is None:
             self.status_label.setText("Status: No ECG data to plot.")
             return

        start_end = self.sample_input.text().split(',')
        start_sample = int(start_end[0].strip())
        end_sample = int(start_end[1].strip())
    
        distance = int(self.distance_input.text())
        height = int(self.height_input.text())

        ecg_segment = self.filtered_ecg_signal[start_sample:end_sample]
        r_peaks, _ = find_peaks(ecg_segment, distance=distance, height=height)
    
        # Calculate BPM
        rr_intervals = np.diff(r_peaks) / 256.0  # Convert from samples to seconds
        if len(rr_intervals) > 0:
            heart_rate = 60.0 / np.mean(rr_intervals)  # Convert to BPM
            bpm_text = f'Estimated Heart Rate: {heart_rate:.2f} BPM'
            self.status_label.setText(bpm_text)
        else:
            bpm_text = "No peaks detected"
    
        plt.figure(figsize=(10, 4))
        plt.plot(ecg_segment, label='Filtered ECG Signal')
        plt.plot(r_peaks, ecg_segment[r_peaks], 'rx', label='Detected R-peaks')
        plt.title(f'ECG Signal with Detected R-Peaks (Samples {start_sample} to {end_sample})')
        plt.xlabel('Time (samples)')
        plt.ylabel('Amplitude')
        plt.legend()
        plt.figtext(0.15, 0.85, bpm_text, fontsize=12, color='blue')
        plt.show()

    def plot_ppg_signal(self):
        if self.filtered_ppg_signal is None:
             self.status_label.setText("Status: No PPG data to plot.")
             return

        start_end = self.sample_input.text().split(',')
        start_sample = int(start_end[0].strip())
        end_sample = int(start_end[1].strip())
    
        distance = int(self.distance_input.text())
        height = int(self.height_input.text())

        ppg_segment = self.filtered_ppg_signal[start_sample:end_sample]
        p_peaks, _ = find_peaks(ppg_segment, distance=distance, height=height)
    
        # Calculate BPM
        rr_intervals = np.diff(p_peaks) / 256.0  # Convert from samples to seconds
        if len(rr_intervals) > 0:
            heart_rate = 60.0 / np.mean(rr_intervals)  # Convert to BPM
            bpm_text = f'Estimated Heart Rate: {heart_rate:.2f} BPM'
            self.status_label.setText(bpm_text)
        else:
            bpm_text = "No peaks detected"
    
        plt.figure(figsize=(10, 4))
        plt.plot(ppg_segment, label='Filtered PPG Signal')
        plt.plot(p_peaks, ppg_segment[p_peaks], 'gx', label='Detected P-peaks')
        plt.title(f'PPG Signal with Detected Peaks (Samples {start_sample} to {end_sample})')
        plt.xlabel('Time (samples)')
        plt.ylabel('Amplitude')
        plt.legend()
        plt.figtext(0.15, 0.85, bpm_text, fontsize=12, color='blue')
        plt.show()

    def plot_psd(self):
        if self.filtered_ecg_signal is None:
            self.status_label.setText("Status: No ECG data to plot PSD.")
            return

        f, Pxx = welch(self.filtered_ecg_signal, fs=256.0, nperseg=1024)
        
        plt.figure(figsize=(10, 4))
        plt.semilogy(f, Pxx)
        plt.title('Power Spectral Density of ECG Signal')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Power')
        plt.show()

    def save_plot(self):
        save_dialog = QFileDialog()
        file_name, _ = save_dialog.getSaveFileName(self, "Save Plot", "", "PNG Files (*.png);;All Files (*)")
        if file_name:
            plt.gcf().savefig(file_name, bbox_inches='tight')  # Save the current figure
            self.status_label.setText(f'Plot saved as: {file_name}')
        else:
            self.status_label.setText("Status: Save operation canceled.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SignalAnalyzer()
    ex.show()
    sys.exit(app.exec_())
