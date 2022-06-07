# Govee API
# https://govee-public.s3.amazonaws.com/developer-docs/GoveeDeveloperAPIReference.pdf
# API v1.7

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

class Govee:
    """Govee API client"""

    def __init__(
        self,
        api_key: str,
    ) -> None:
        self._api_key = api_key
        self._devices = {}
        
        pass

def get_devices() -> list:
    resp = requests.get(API['get_devices'], headers={"Govee-API-Key": API['api_key']})
    resp.raise_for_status()
    return resp.json()['data']['devices']

def get_avail_controls(device: dict):
    print(device['supportCmds'])


def power_device(device, cmd = "off"):
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
    # Get my devices
    devices = get_devices()
    light_stick = devices[0]

    # Perform actions on devices
    power_device(light_stick, "on")
    time.sleep(5) # Wait 5 seconds
    power_device(light_stick, "off")
    



if __name__ == '__main__':
    main()
