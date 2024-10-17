import time

import requests
from datetime import datetime
import smtplib

MY_LAT = 43.897545
MY_LONG = -78.942932
EMAIL_ADDRESS = "email@gmail.com"
PASSWORD = "password"
GMAIL_HOST= "smtp.gmail.com"
PORT = 587

def iss_is_near():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if abs(iss_latitude - MY_LAT) <= 100 and abs(iss_longitude - MY_LONG) <= 100:
        return True


def is_nighttime():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()

    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()
    current_hour = int(time_now.hour)
    print(f"The current hour is: {current_hour}.")
    if current_hour >= sunset or current_hour <= sunrise:
        return True


while True:
    if iss_is_near() and is_nighttime():
            with smtplib.SMTP(GMAIL_HOST, PORT) as connection:
                connection.starttls()
                connection.login(user=EMAIL_ADDRESS, password=PASSWORD)
                connection.sendmail(from_addr=EMAIL_ADDRESS, to_addrs=EMAIL_ADDRESS,
                                    msg=f"Subject: ISS Nearby!\n\n The ISS is overhead! Look up to see!👆🏾\n\n"
                                        f"- Sent from Billie's Python Lair.")
    time.sleep(60)




