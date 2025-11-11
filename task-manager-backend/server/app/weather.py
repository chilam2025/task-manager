from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        'message': 'Welcome to the Mock API Suite',
        'status': 'running'
    })


@app.route('/api/weather/current')
def current_weather():
    city = request.args.get('city', 'Unknown')
    sample_data = {
        'London': {'temperature': '15°C', 'condition': 'Cloudy', 'humidity': '78%'},
        'Paris': {'temperature': '18°C', 'condition': 'Sunny', 'humidity': '65%'},
        'New York': {'temperature': '20°C', 'condition': 'Rainy', 'humidity': '82%'}
    }

    if city in sample_data:
        return jsonify({
            'city': city,
            **sample_data[city]
        })
    else:
        return jsonify({'error': 'City not found'}), 404


@app.route('/api/weather/forecast')
def weather_forecast():
    city = request.args.get('city', 'Unknown')
    days = int(request.args.get('days', 3))

    forecast_data = {
        'Paris': [
            {'day': 1, 'temperature': '18°C', 'condition': 'Sunny'},
            {'day': 2, 'temperature': '17°C', 'condition': 'Partly Cloudy'},
            {'day': 3, 'temperature': '19°C', 'condition': 'Clear'}
        ],
        'London': [
            {'day': 1, 'temperature': '15°C', 'condition': 'Rainy'},
            {'day': 2, 'temperature': '16°C', 'condition': 'Cloudy'},
            {'day': 3, 'temperature': '14°C', 'condition': 'Foggy'}
        ]
    }

    if city in forecast_data:
        return jsonify({
            'city': city,
            'forecast': forecast_data[city][:days]
        })
    else:
        return jsonify({'error': 'City not found'}), 404



if __name__ == '__main__':
    app.run(debug=True, port=8000)
