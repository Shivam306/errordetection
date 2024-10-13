from flask import Flask, render_template, request, jsonify
import csv
import os
from datetime import datetime

app = Flask(__name__)


# Function to get the path for the current month's folder
def get_csv_file_path(process_name):
    # Get the current month and day
    current_month = datetime.now().strftime('%B')
    current_day = datetime.now().strftime('%d %b')

    # Path to the csv_data folder
    base_folder = os.path.join(os.getcwd(), 'csv_data')

    # Create the base folder if it doesn't exist
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)

    # Path to the current month folder
    month_folder = os.path.join(base_folder, current_month)

    # Create the month folder if it doesn't exist
    if not os.path.exists(month_folder):
        os.makedirs(month_folder)

    # Path to the date folder
    date_folder = os.path.join(month_folder, current_day)

    # Create the date folder if it doesn't exist
    if not os.path.exists(date_folder):
        os.makedirs(date_folder)

    # Path to the CSV file inside the date folder
    csv_file_path = os.path.join(date_folder, f"{process_name}.csv")

    return csv_file_path


@app.route('/')
def index():
    num_frames = 7  # Fixed number of frames for SPM
    return render_template('index.html', num_frames=num_frames)


@app.route('/second')
def second():
    num_frames = 8  # Fixed number of frames for CNC
    return render_template('second.html', num_frames=num_frames)


@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Get the form data from the request
        data = request.form.to_dict()

        # Prepare a list to hold CSV row values
        csv_row = []

        # Get the process name and index from the form data
        process_name = data.get(f'Process_Name{data["index"]}')

        # Extract relevant form data into the csv_row
        for key in data:
            if 'index' not in key:  # Exclude the index
                csv_row.append(data[key])

        # Get the path for the CSV file
        csv_file_path = get_csv_file_path(process_name)

        # Write to the CSV file
        with open(csv_file_path, mode='a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(csv_row)

        return jsonify({'status': 'success', 'message': 'Data submitted successfully!'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
