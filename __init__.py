import csv

class SignalData:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = []
        self.headers = []
        self.read_csv()

    def read_csv(self):
        """Reads the CSV file and stores the data in a list of dictionaries."""
        with open(self.filepath, mode='r') as file:
            csv_reader = csv.DictReader(file)
            self.headers = csv_reader.fieldnames  
            for row in csv_reader:
                
                self.data.append({
                    'time': float(row['Time (s)']),
                    'frequency': float(row['Frequency (MHz)']),
                    'level': float(row['Level (dBm)'])
                })

    def get_data(self):
        """Returns the stored data."""
        return self.data

    def get_unique_frequencies(self):
        """Returns the unique frequencies in the data."""
        return sorted(set(item['frequency'] for item in self.data))

    def filter_by_time(self, time_value):
        """Filters the data by a specific time and returns measurements at that time."""
        return [item for item in self.data if item['time'] == time_value]

    def filter_by_frequency(self, frequency_value):
        """Filters the data by a specific frequency and returns measurements at that frequency."""
        return [item for item in self.data if item['frequency'] == frequency_value]


if __name__ == '__main__':
    # Provide the path to your CSV file
    filepath = 'data/data1.csv'
    signal_data = SignalData(filepath)

    # Access the data
    print("Unique frequencies in the data:", signal_data.get_unique_frequencies())

    # Filter by a specific time (e.g., 0.01 seconds)
    time_data = signal_data.filter_by_time(0.01)
    print(f"Data at time 0.01 seconds: {time_data}")

    # Filter by a specific frequency (e.g., 100 MHz)
    freq_data = signal_data.filter_by_frequency(100)
    print(f"Data at frequency 100 MHz: {freq_data}")
