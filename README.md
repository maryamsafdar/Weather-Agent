# Weather App with City Images

This is a Streamlit application that allows users to enter a city name and view the current weather information along with an image of the city, fetched using the OpenWeatherMap and Unsplash APIs.

## Features

- Get real-time weather data (temperature, humidity, wind speed, and description).
- Fetch images of the city using the Unsplash API.
- User-friendly interface with Streamlit.

## Prerequisites

- Python 3.7 or higher.
- Unsplash API key: [Get an Unsplash API key](https://unsplash.com/developers).
- OpenWeatherMap API key: [Get an OpenWeatherMap API key](https://openweathermap.org/api).

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/yourusername/weather-app
    cd weather-app
    ```

2. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the root directory and add your API keys:

    ```env
    OPENWEATHER_API_KEY=your_openweather_api_key
    UNSPLASH_ACCESS_KEY=your_unsplash_access_key
    ```

4. Run the Streamlit application:

    ```bash
    streamlit run app.py
    ```

## Usage

1. Open the Streamlit app in your browser.
2. Enter the name of the city you want to get the weather information for.
3. The app will display the current weather details along with an image of the city.

## Project Structure

- `app.py`: The main application script.
- `README.md`: Documentation for the project.
- `requirements.txt`: List of Python packages required to run the application.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [OpenWeatherMap](https://openweathermap.org/) for weather data.
- [Unsplash](https://unsplash.com/developers) for beautiful city images.
- [Streamlit](https://streamlit.io/) for building a user-friendly interface.

## Contact

For any inquiries, please contact [your-email@example.com].
