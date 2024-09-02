import os
from flask import Flask, request, jsonify
import requests
import redis
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import json
from datetime import timedelta

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Setup rate limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per day", "10 per hour"]
)

# Visual Crossing API endpoint
VISUAL_CROSSING_API_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"

# Setup Redis connection
redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=os.getenv('REDIS_PORT', 6379),
    db=0,
    decode_responses=True
)

CACHE_EXPIRATION = timedelta(hours=12)  # Cache data for 12 hours

def get_weather_from_api(city):
    api_key = os.getenv('VISUAL_CROSSING_API_KEY')
    
    if not api_key:
        raise Exception("API key not configured")

    # Construct the URL for the Visual Crossing API
    url = f"{VISUAL_CROSSING_API_URL}/{city}?unitGroup=metric&key={api_key}"

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

    return result

@app.route('/weather/<city>', methods=['GET'])
@limiter.limit("10 per minute")
def get_weather(city):
    try:
        # Try to get data from cache
        cached_data = redis_client.get(city)
        if cached_data:
            return jsonify(json.loads(cached_data))

        # If not in cache, fetch from API
        weather_data = get_weather_from_api(city)

        # Store in cache
        redis_client.setex(city, CACHE_EXPIRATION, json.dumps(weather_data))

        return jsonify(weather_data)

    except redis.RedisError as e:
        app.logger.error(f"Redis error: {str(e)}")
        # If Redis is down, fetch directly from API without caching
        try:
            weather_data = get_weather_from_api(city)
            return jsonify(weather_data)
        except Exception as e:
            return jsonify({"error": f"Failed to fetch weather data: {str(e)}"}), 500

    except requests.RequestException as e:
        return jsonify({"error": f"Failed to fetch weather data: {str(e)}"}), 500

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)