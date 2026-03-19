import streamlit
import requests

streamlit.title("EcoMute Trip Duration Predictor")

streamlit.write("Adjust the sliders below to estimate how long a bike trip will take.")

distance_km = streamlit.slider(
    "Distance (km)",
    min_value=1.0,
    max_value=100.0,
    value=10.0,
    step=0.5,
)

battery_level = streamlit.slider(
    "Battery Level (%)",
    min_value=0.0,
    max_value=100.0,
    value=80.0,
    step=1.0,
)

if streamlit.button("Predict Trip Duration"):
    api_url = "http://127.0.0.1:8000/predict/"

    payload = {
        "distance_km": distance_km,
        "battery_level": battery_level,
    }

    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()

        result = response.json()
        estimated_minutes = result["estimated_minutes"]

        streamlit.metric(
            label="Estimated Trip Duration",
            value=f"{estimated_minutes} minutes",
        )

    except requests.exceptions.ConnectionError:
        streamlit.error(
            "Could not connect to the API. Make sure your FastAPI server is running."
        )

    except requests.exceptions.HTTPError as error:
        streamlit.error(f"API returned an error: {error}")