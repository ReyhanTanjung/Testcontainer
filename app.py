from flask import Flask, jsonify, Response
from datetime import datetime, timedelta
import random
import json

app = Flask(__name__)

# Fungsi untuk membuat data timeseries dengan interval 1 jam dan format JSON yang ditentukan
def generate_timeseries_data(location, num_points=24, interval='10_minutes'):
    start_time = datetime.now() - timedelta(hours=num_points)
    timeseries_data = []

    for i in range(num_points):
        if interval == 'hourly':
            timestamp = start_time - timedelta(hours=i)
        elif interval == '10_minutes':
            timestamp = start_time - timedelta(minutes=i * 10)

        data_point = {
            "active_energy_export": random.randint(0, 100000),
            "reactive_energy_import": random.randint(80000, 100000),
            "reactive_energy_export": random.randint(27000000, 28000000),
            "apparent_energy_import": random.randint(100000000, 110000000),
            "apparent_energy_export": random.randint(0, 1000),
            "instantaneous_voltage_L1": round(random.uniform(220.0, 230.0), 3),
            "instantaneous_voltage_L2": round(random.uniform(220.0, 230.0), 3),
            "instantaneous_voltage_L3": round(random.uniform(220.0, 230.0), 3),
            "instantaneous_current_L1": round(random.uniform(0.3, 0.5), 3),
            "instantaneous_current_L2": round(random.uniform(0.3, 0.5), 3),
            "instantaneous_current_L3": round(random.uniform(0.3, 0.5), 3),
            "instantaneous_net_frequency": round(random.uniform(49.5, 50.5), 2),
            "instantaneous_power_factor": round(random.uniform(0.08, 1.0), 4),
            "create_date": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "location": location
        }

        timeseries_data.append(data_point)

    return timeseries_data

# Fungsi untuk mengonversi setiap data point ke JSON format dengan pretty-print
def convert_to_custom_json(data):
    json_data = json.dumps(data, indent=4)
    custom_json = json_data.replace('"type":', 'type:').replace('"data":', 'data:')
    return custom_json

# Endpoint GET untuk mengirim data secara terpisah satu per satu
@app.route('/api/timeseries/location/<location>', methods=['GET'])
def get_timeseries_data_stream(location):
    data = generate_timeseries_data(location=location, num_points=24, interval='10_minutes')
    
    def generate():
        for data_point in data:
            # Setiap objek dikirim satu per satu dalam format JSON
            response_data = {
                "data": data_point,
                "type": "uplink"
            }
            yield convert_to_custom_json(response_data) + '\n'
    
    return Response(generate(), mimetype='application/json')

# Endpoint untuk mendapatkan data paling terbaru
@app.route('/api/timeseries/location/<location>/lasthistory', methods=['GET'])
def get_last_history(location):
    data = generate_timeseries_data(location=location, num_points=1)
    response_data = {
        "data": data[-1],
        "type": "uplink"
    }
    custom_json = convert_to_custom_json(response_data)
    return Response(custom_json, mimetype='application/json')

# Endpoint GET untuk lokasi A, B, C (per lokasi, interval 1 jam untuk setiap data point)
@app.route('/api/timeseries/location/<location>', methods=['GET'])
def get_timeseries_data(location):
    data = generate_timeseries_data(location=location, num_points=24, interval='10_minutes')
    response_data = {
        "data": data,
        "type": "uplink"
    }
    custom_json = convert_to_custom_json(response_data)
    return Response(custom_json, mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

