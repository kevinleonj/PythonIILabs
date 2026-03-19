import numpy
import pandas
from sklearn.linear_model import LinearRegression
import joblib
import os

numpy.random.seed(42)

number_of_samples = 1000

distance_km = numpy.random.uniform(1, 50, number_of_samples)
battery_level = numpy.random.uniform(10, 100, number_of_samples)
trip_duration_minutes = (distance_km * 3) - (battery_level * 0.1) + numpy.random.normal(0, 2, number_of_samples)

training_data = pandas.DataFrame({
    "distance_km": distance_km,
    "battery_level": battery_level,
    "trip_duration_minutes": trip_duration_minutes,
})

input_features = training_data[["distance_km", "battery_level"]]
target = training_data["trip_duration_minutes"]

model = LinearRegression()
model.fit(input_features, target)

sample_prediction = model.predict(pandas.DataFrame([[10, 80]], columns=["distance_km", "battery_level"]))
print(f"Sample prediction: 10 km with 80% battery = {sample_prediction[0]:.1f} minutes")

script_directory = os.path.dirname(os.path.abspath(__file__))
model_file_path = os.path.join(script_directory, "trip_predictor.joblib")

joblib.dump(model, model_file_path)
print(f"Model saved to: {model_file_path}")