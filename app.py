from flask import Flask, render_template, request
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

#  OpenWeatherMap API Key

API_KEY = os.getenv('API_KEY')

def format_time(unix_timestamp, timezone_offset):
    # Adjust UTC time to local city time
    local_time = datetime.utcfromtimestamp(unix_timestamp + timezone_offset)
    return local_time.strftime('%H:%M:%S')

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    city = None
    error_message = None

    if request.method == 'POST':
        city = request.form.get('city').strip() # .strip() removes accidental spaces
        
        if not city:
            error_message = "Please enter a city name."
        else:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            try:
                response = requests.get(url).json()
                
                if response.get('cod') == 200:
                    offset = response['timezone']
                    weather_data = {
                        'temp': response['main']['temp'],
                        'humidity': response['main']['humidity'],
                        'sunrise': format_time(response['sys']['sunrise'], offset),
                        'sunset': format_time(response['sys']['sunset'], offset),
                         'condition': response['weather'][0]['main']
                        
                    }
                 
                else:
                    # This catches "City Not Found" (Error 404)
                    error_message = f"City '{city}' not found. Please try again."
            
            except requests.exceptions.RequestException:
                error_message = "Could not connect to the weather service."

    return render_template('index.html', weather=weather_data, city=city, error=error_message)


if __name__ == '__main__':
    app.run(debug=True)