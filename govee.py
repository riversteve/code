# Govee API
# https://govee-public.s3.amazonaws.com/developer-docs/GoveeDeveloperAPIReference.pdf

from dotenv import load_dotenv
import json
import os
import requests
import time

load_dotenv()
API_URL = "https://developer-api.govee.com"
API = {
    'api_key'               : os.environ.get('GOVEE_API_KEY'),
    'get_devices'           : API_URL + "/v1/devices",
    'put_device_control'    : API_URL + "/v1/devices/control",
    'get_device_state'      : API_URL + "/v1/devices/state?",

}

def get_devices() -> list:
    resp = requests.get(API['get_devices'], headers={"Govee-API-Key": API['api_key']})
    resp.raise_for_status()
    return resp.json()['data']['devices']

def get_avail_controls(device: dict):
    print(device['supportCmds'])


def power_device(device, cmd):
    headers = {
        "Govee-API-Key": API['api_key'],
        "Content-Type": "application/json",
    }
    params = {
        'device'    : device['device'],
        'model'     : device['model'],
        'cmd'       : {
            "name": "turn",
            "value": cmd
        }
    }
    resp = requests.put(API['put_device_control'], headers=headers, json=params)
    pass


def main():
    devices = get_devices()

    power_device(devices[-1], "on")
    time.sleep(5)
    power_device(devices[-1], "off")
    



if __name__ == '__main__':
    main()
