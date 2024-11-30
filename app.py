import streamlit as st
import requests
import random
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Weather Forecast",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        font-family: 'Poppins', sans-serif;
    }
    
    .header {
        background: linear-gradient(160deg, #0093E9 0%, #80D0C7 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    .weather-card {
        background: rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        margin-bottom: 1rem;
        color: white;
    }
    
    .city-name {
        font-size: 1.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
        color: white;
    }
    
    .temperature {
        font-size: 3.5rem;
        font-weight: bold;
        text-align: center;
        margin: 1rem 0;
        color: white;
    }
    
    .weather-description {
        font-size: 1.2rem;
        text-align: center;
        margin-bottom: 2rem;
        color: #E0E0E0;
    }
    
    .sidebar {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #0093E9 0%, #80D0C7 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 10px;
        font-weight: bold;
        width: 100%;
    }
    
    .footer {
        text-align: center;
        padding: 1rem;
        color: white;
        background: rgba(0, 0, 0, 0.2);
        position: fixed;
        bottom: 0;
        width: 100%;
        left: 0;
    }
</style>
""", unsafe_allow_html=True)

def get_weather_data(city):
    """Fetch weather data from OpenWeatherMap API"""
    api_key = "c4647569cd33e1735940c1c0809bf2a2"
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    try:
        response = requests.get(
            base_url,
            params={
                "q": city,
                "appid": api_key,
                "units": "metric"
            }
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error fetching weather data: {str(e)}")
        return None

def create_weather_card(data, title):
    """Create weather card layout with wind, humidity, and other details"""
    city = data.get('name', '')
    temp = data['main'].get('temp', '--')
    humidity = data['main'].get('humidity', '--')
    wind_speed = data['wind'].get('speed', '--')
    description = data['weather'][0].get('description', 'Unknown').capitalize()
    
    st.markdown(f"""
    <div class="weather-card">
        <h2 style="text-align: center; color: white;">{title}</h2>
        <div class="city-name">{city}</div>
        <div class="temperature">{temp}°C</div>
        <div class="weather-description">{description}</div>
        <div class="weather-description"><strong>Humidity:</strong> {humidity}%</div>
        <div class="weather-description"><strong>Wind Speed:</strong> {wind_speed} m/s</div>
    </div>
    """, unsafe_allow_html=True)

def predict_weather(current_weather):
    """Generate weather prediction with random fluctuations"""
    return {
        'name': current_weather['name'],
        'main': {
            'temp': round(current_weather['main']['temp'] + random.uniform(-2, 2), 1),
            'humidity': min(100, max(0, current_weather['main']['humidity'] + random.randint(-10, 10))),
            'pressure': current_weather['main']['pressure'] + random.randint(-20, 20),
            'feels_like': round(current_weather['main']['feels_like'] + random.uniform(-2, 2), 1)
        },
        'wind': {
            'speed': max(0, round(current_weather['wind']['speed'] + random.uniform(-1, 1), 2))
        },
        'weather': [
            {
                'description': current_weather['weather'][0]['description']
            }
        ]
    }

def main():
    # Header
    st.markdown("""
        <div class="header">
            <h1>🌤️ Weather Forecast</h1>
            <p>Real-time weather updates and predictions</p>
        </div>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown('<div class="sidebar">', unsafe_allow_html=True)
        city = st.text_input("Enter City Name", "Brahmapur")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Current time
        st.markdown('<div class="sidebar">', unsafe_allow_html=True)
        st.write("⏰ Current Time")
        st.write(datetime.now().strftime("%H:%M:%S"))
        st.markdown("</div>", unsafe_allow_html=True)

    if city:
        with st.spinner("Fetching weather data..."):
            current_weather = get_weather_data(city)
            
            if current_weather and current_weather.get('cod') == 200:
                col1, col2 = st.columns(2)
                
                with col1:
                    create_weather_card(current_weather, "Current Weather")
                
                with col2:
                    predicted_weather = predict_weather(current_weather)
                    create_weather_card(predicted_weather, "Predicted Weather")
            else:
                st.error("Unable to fetch weather data. Please check the city name and try again.")

    # Refresh button
    if st.sidebar.button("🔄 Refresh"):
        st.rerun()

    # Footer
    st.markdown(f"""
        <div class="footer">
            <p>Made with ❤️ by NIST Project Group Team</p>
            <p style="font-size: 0.8em;">Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()


# run the code "streamlit run app.py"