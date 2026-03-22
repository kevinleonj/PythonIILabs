import time
import random
import requests
import streamlit as st

st.set_page_config(
    page_title="EcoMute Trip Planner",
    page_icon="\U0001F6B4",
    layout="centered",
)

st.markdown("""
    <style>
    .big-title { font-size: 3rem; font-weight: 800; color: #1D9E75; margin-bottom: 0; }
    .subtitle { font-size: 1.1rem; color: #aaa; margin-bottom: 0.5rem; }
    .tagline { font-size: 1.3rem; font-weight: 600; color: #fff; margin-bottom: 1.5rem; }
    .about-box { background: #0e1117; border-left: 4px solid #1D9E75;
                 border-radius: 8px; padding: 1rem 1.25rem; margin-bottom: 1.5rem;
                 color: #ccc; font-size: 0.95rem; line-height: 1.7; }
    .bike-card { background: #0e1117; border: 1px solid #1D9E75;
                 border-radius: 10px; padding: 0.75rem 1rem; margin-bottom: 0.5rem;
                 color: #ccc; font-size: 0.88rem; line-height: 1.6; }
    .quote-box { background: #0e1117; border-left: 4px solid #534AB7;
                 border-radius: 8px; padding: 1rem 1.25rem; margin-top: 1rem;
                 color: #bbb; font-size: 0.95rem; font-style: italic; }
    .fire { font-size: 2rem; animation: pulse 0.8s infinite alternate; display: inline-block; }
    @keyframes pulse { from { transform: scale(1); } to { transform: scale(1.3); } }
    div.stButton > button { background-color: #1D9E75; color: white; border: none;
                            border-radius: 12px; padding: 0.75rem 2rem;
                            font-size: 1.1rem; font-weight: 600; width: 100%; }
    div.stButton > button:hover { background-color: #0F6E56; }
    </style>
""", unsafe_allow_html=True)

BIKE_TYPES = {
    "Small City (300-400 Wh)": {
        "wh": "300-400 Wh",
        "max_km": 40.0,
        "max_miles": 25.0,
        "desc": "Perfect for short urban commutes. Lightweight and nimble.",
        "range_km": "24-40 km",
        "range_miles": "15-25 miles",
    },
    "Standard Commuter (400-600 Wh)": {
        "wh": "400-600 Wh",
        "max_km": 72.0,
        "max_miles": 45.0,
        "desc": "The everyday workhorse. Great balance of range and weight.",
        "range_km": "40-72 km",
        "range_miles": "25-45 miles",
    },
    "Premium Long-Range (600-900 Wh+)": {
        "wh": "600-900 Wh+",
        "max_km": 112.0,
        "max_miles": 70.0,
        "desc": "Built for long adventures. Maximum range, maximum freedom.",
        "range_km": "64-112+ km",
        "range_miles": "40-70+ miles",
    },
}

LONG_QUOTES = [
    '"A bicycle ride around the world begins with a single pedal stroke." Long rides are about endurance, mental strength, and finding freedom on two wheels.',
    '"Four wheels move the body, but two wheels move the soul." Whether tackling steep climbs or cruising, focus on the journey, embrace the sweat.',
]

st.markdown('<p class="big-title">EcoMute</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">AI-powered trip duration estimator</p>', unsafe_allow_html=True)
st.markdown('<p class="tagline">Don\'t wonder anymore - know exactly how long your ride will take.</p>', unsafe_allow_html=True)

st.markdown("""
<div class="about-box">
    <strong style="color:#1D9E75;">What is EcoMute?</strong><br>
    EcoMute is a smart e-bike platform that helps urban commuters plan their trips with confidence.
    Our AI engine analyses your route distance and your bike's current battery level to predict
    your estimated travel time - so you always arrive on time, stress-free.<br><br>
    <strong style="color:#1D9E75;">Who is it for?</strong><br>
    Anyone commuting, exercising, or exploring the city on an electric bike who wants
    a data-driven estimate before they set off.
</div>
""", unsafe_allow_html=True)

st.divider()

st.markdown("#### Select your bike type")
bike_choice = st.selectbox(
    "Bike type",
    options=list(BIKE_TYPES.keys()),
    label_visibility="collapsed",
)
bike = BIKE_TYPES[bike_choice]

st.markdown(f"""
<div class="bike-card">
    <strong style="color:#1D9E75;">{bike_choice}</strong> &nbsp;&middot;&nbsp; {bike['wh']}<br>
    {bike['desc']}<br>
    <span style="color:#aaa;">Typical range: <strong style="color:#fff;">{bike['range_km']}</strong>
    &nbsp;/&nbsp; <strong style="color:#fff;">{bike['range_miles']}</strong></span>
</div>
""", unsafe_allow_html=True)

st.divider()

unit = st.radio("Distance unit", ["km", "miles"], horizontal=True)

max_dist = bike["max_miles"] if unit == "miles" else bike["max_km"]
long_threshold = 12.4 if unit == "miles" else 20.0
default_dist = min(6.0 if unit == "miles" else 10.0, max_dist)

col1, col2 = st.columns(2)
with col1:
    distance = st.slider(f"Distance ({unit})", 1.0, max_dist, default_dist, step=0.5)
with col2:
    battery = st.slider("Battery level (%)", 0.0, 100.0, 80.0, step=1.0)

distance_km = distance * 1.60934 if unit == "miles" else distance

if battery < 30:
    st.warning("Low battery - your trip may take considerably longer.")

if distance > long_threshold:
    st.warning(
        f"You've selected a long distance ({distance} {unit}). "
        f"Make sure your battery is fully charged and you have everything you need. "
        f"Consider bringing a spare charger or planning a charging stop!"
    )

st.divider()

if st.button("Predict my trip duration", type="primary", use_container_width=True):
    payload = {"distance_km": round(distance_km, 2), "battery_level": battery}
    try:
        with st.spinner("Our AI is calculating your trip..."):
            time.sleep(0.7)
            response = requests.post("http://127.0.0.1:8000/predict/", json=payload)

        if response.status_code == 200:
            mins = response.json()["estimated_minutes"]
            hrs = int(mins // 60)
            rem = int(mins % 60)
            time_str = f"{hrs}h {rem}m" if hrs > 0 else f"{int(mins)} min"

            if mins < 30:
                st.success("**Fast ride** - You'll be there in no time!")
                st.balloons()
                st.markdown("#### Short ride - pedal hard and enjoy the breeze!")

            elif mins < 60:
                st.success("**Smooth cruiser** - A perfect ride, not too short, not too long.")
                st.balloons()
                st.markdown("#### Medium ride - find your rhythm and enjoy the city!")

            else:
                st.success("**Epic journey ahead** - This is where legends are made!")
                st.markdown(
                    '<div style="text-align:center; margin: 0.5rem 0;">'
                    '<span class="fire">&#128293;</span>'
                    '<span class="fire" style="animation-delay:0.2s">&#128293;</span>'
                    '<span class="fire" style="animation-delay:0.4s">&#128293;</span>'
                    '</div>',
                    unsafe_allow_html=True
                )
                st.markdown("#### Long ride - endurance mode activated!")
                quote = random.choice(LONG_QUOTES)
                st.markdown(f'<div class="quote-box">{quote}</div>', unsafe_allow_html=True)

            st.divider()
            _, c1, c2, c3, _ = st.columns([1, 2, 2, 2, 1])
            c1.metric("Duration", time_str)
            c2.metric("Distance", f"{distance} {unit}")
            c3.metric("Battery", f"{battery}%")

            if unit == "miles":
                st.caption(f"*Calculated using {round(distance_km, 1)} km internally*")

        else:
            st.error("Could not reach the API. Is uvicorn running?")

    except requests.exceptions.RequestException as e:
        st.error(f"Connection failed: {e}")