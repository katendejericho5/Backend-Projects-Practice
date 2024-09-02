import os
from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Setup rate limiting
limiter = Limiter(
    get_remote_address,
    default_limits=["100 per day", "10 per hour"]
)
limiter.init_app(app)

# Visual Crossing API endpoint
VISUAL_CROSSING_API_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"

@app.route('/weather/<city>', methods=['GET'])
@limiter.limit("5 per minute")
def get_weather(city):
    api_key = os.getenv('VISUAL_CROSSING_API_KEY')
    
    if not api_key:
        return jsonify({"error": "API key not configured"}), 500

    # Construct the URL for the Visual Crossing API
    url = f"{VISUAL_CROSSING_API_URL}/{city}?unitGroup=metric&key={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad responses
        weather_data = response.json()

        # Extract relevant information
        current = weather_data.get('currentConditions', {})
        forecast = weather_data.get('days', [{}])[0]  # Get today's forecast

        result = {
            "city": city,
            "temperature": current.get('temp'),
            "condition": current.get('conditions'),
            "humidity": current.get('humidity'),
            "wind_speed": current.get('windspeed'),
            "forecast": {
                "max_temp": forecast.get('tempmax'),
                "min_temp": forecast.get('tempmin'),
                "description": forecast.get('description')
            }
        }

        return jsonify(result)

    except requests.RequestException as e:
        return jsonify({"error": f"Failed to fetch weather data: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
