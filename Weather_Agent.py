import streamlit as st
import os
import requests
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_core.runnables.graph import MermaidDrawMethod
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO

# Load environment variables
load_dotenv()
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

# Define the state structure
class State(TypedDict):
    city: str
    temperature: float
    humidity: float
    wind_speed: float
    description: str
    image_url: str

def get_user_input_node(state: State):
    ''' Get user input for city '''
    state["city"] = st.text_input("Enter the name of the city:", "New York")
    return state

def fetch_weather_node(state: State):
    ''' Fetch weather data from the OpenWeatherMap API '''
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': state["city"],
        'appid': OPENWEATHER_API_KEY,
        'units': 'metric'
    }
    response = requests.get(base_url, params=params)
    data = response.json()

    if response.status_code == 200:
        state.update({
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "description": data["weather"][0]["description"]
        })
    else:
        state.update({
            "temperature": None,
            "humidity": None,
            "wind_speed": None,
            "description": "City not found or API error"
        })
    return state

def fetch_city_image_node(state: State):
    '''Fetch a city image using the Unsplash API.'''
    base_url = f"https://api.unsplash.com/photos/random?query={state['city']}&client_id={UNSPLASH_ACCESS_KEY}"
    response = requests.get(base_url)

    if response.status_code == 200:
        data = response.json()
        state["image_url"] = data['urls']['regular']
    else:
        state["image_url"] = None
    return state

def display_weather_node(state: State):
    '''Display weather information and the city image.'''
    if state['temperature'] is not None:
        st.write(f"### Weather in {state['city']}")
        st.write(f"**Temperature:** {state['temperature']}°C")
        st.write(f"**Humidity:** {state['humidity']}%")
        st.write(f"**Wind Speed:** {state['wind_speed']} m/s")
        st.write(f"**Description:** {state['description']}")
    else:
        st.error(f"Error: {state['description']}")

    if state["image_url"]:
        image_response = requests.get(state["image_url"])
        image = Image.open(BytesIO(image_response.content))
        st.image(image, caption=f"{state['city']}", use_column_width=True)
    return state

# Create the LangGraph workflow
workflow = StateGraph(State)

# Add nodes to the graph
workflow.add_node("get_user_input", get_user_input_node)
workflow.add_node("fetch_weather", fetch_weather_node)
workflow.add_node("fetch_city_image", fetch_city_image_node)
workflow.add_node("display_weather", display_weather_node)

# Define the flow between nodes
workflow.set_entry_point("get_user_input")
workflow.add_edge("get_user_input", "fetch_weather")
workflow.add_edge("fetch_weather", "fetch_city_image")
workflow.add_edge("fetch_city_image", "display_weather")
workflow.add_edge("display_weather", END)

# Compile the graph
app = workflow.compile()

# Streamlit app UI
st.title("City Weather and Image Viewer 🌤️🖼️")
st.write("Get the current weather of any city along with a beautiful image of the location. Simply enter the name of the city below, and hit the button to see the results!")

# Invoke the workflow if the user presses the button
if st.button("Get Weather and Image"):
    initial_state = {"city": "", "temperature": 0, "humidity": 0, "wind_speed": 0, "description": "", "image_url": ""}
    result = app.invoke(initial_state)
