import requests
import time
from suntime import Sun
from datetime import datetime, timedelta

session = requests.Session()
session.verify = True
sun = Sun(40.72118, -73.98347)
now = datetime.now().astimezone()

def send_command(action):
    url = f'http://192.168.1.174:8838/neo/v1/transmit?command=008.211-15-{action}&id=CL8oIvtpXVGR_QSd9iOgHA'
    r = session.get(url, timeout=5)
    print(f'{now}: {action}')
    if r.status_code != 200:
        print(r.text)

def query_sensor(id):
    url = f'http://192.168.1.125/sensors/{id}'
    data = session.get(url, timeout=5).content
    return int(data)

def check_sun_up():
    sunrise = sun.get_local_sunrise_time()
    sunset = sun.get_local_sunset_time()
    while sunrise < now:
        sunrise += timedelta(days = 1)
    while sunset < now:
        sunset += timedelta(days = 1)
    return sunset < sunrise

can_close = True
can_open = True
sun_up = check_sun_up()

while True:
    now = datetime.now().astimezone()
    last_sun_up = sun_up
    sun_up = check_sun_up()
    if not last_sun_up and sun_up:
        print(f'{now}: sunrise')
        can_open = True
    elif last_sun_up and not sun_up:
        print(f'{now}: sunset')
        can_close = True
    mainroom_co2 = query_sensor('8a93c7')
    bedroom_co2 = query_sensor('dd58e7')
    diff = bedroom_co2 - mainroom_co2
    close_condition = diff > 50
    open_condition = diff < 25
    if can_close and close_condition and not sun_up:
        can_close = False
        send_command('dn')
    if can_open and open_condition and sun_up:
        can_open = False
        send_command('up')
    time.sleep(15)
