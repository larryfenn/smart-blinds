import requests
import time

def send_command(action):
    url = f'http://192.168.1.174:8838/neo/v1/transmit?command=008.211-15-{action}&id=CL8oIvtpXVGR_QSd9iOgHA'
    with requests.Session() as s:
        r = s.get(url)
        if r.status_code != 200:
            print(r.text)

def query_sensor(id):
    url = f'http://192.168.1.125/sensors/{id}'
    with requests.Session() as s:
        data = s.get(url).content
    return int(data)

while True:
    mainroom_co2 = query_sensor('8a93c7')
    bedroom_co2 = query_sensor('dd58e7')
    diff = bedroom_co2 - mainroom_co2
    print(diff)
    if diff > 100:
        send_command('dn')
    if diff < 50:
        send_command('up')
    time.sleep(60)
