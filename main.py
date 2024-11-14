import requests
from datetime import datetime
import time

MY_LAT = 33.5102  # Your latitude
MY_LONG = 36.2913  # Your longitude


def is_iss_overhead():
    # Make a GET request to the ISS position API
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    # Get ISS current latitude and longitude
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # Debug print: Show the ISS position
    print(f"ISS Position: Latitude {iss_latitude}, Longitude {iss_longitude}")


    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        print("ISS is overhead!")
        return True
    print("ISS is not overhead.")
    return False


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    # Get sunrise and sunset data
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()

    # Get the sunrise and sunset hours (in UTC)
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    # Get the current hour (in UTC)
    time_now = datetime.utcnow().hour


    print(f"Current time (UTC): {time_now}")
    print(f"Sunrise: {sunrise}, Sunset: {sunset}")

    # Check if it is night (before sunrise or after sunset)
    if time_now >= sunset or time_now <= sunrise:
        print("It's currently night.")
        return True
    print("It's currently daytime.")
    return False


while True:
    print("Checking ISS position and if it's night...")
    if is_iss_overhead() and is_night():
        print("Look Up👆 The ISS is above you in the sky!")
    else:
        print("No ISS above you right now.")
    time.sleep(60)
