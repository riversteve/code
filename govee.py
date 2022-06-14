# Govee API
# https://govee-public.s3.amazonaws.com/developer-docs/GoveeDeveloperAPIReference.pdf
# API v1.7

from urllib.parse import urlencode
from dotenv import load_dotenv
import json
import os
import requests
import time

# Load API key from .env file
load_dotenv()
API_URL = "https://developer-api.govee.com"
API = {
    'api_key'               : os.environ.get('GOVEE_API_KEY'),
    'get_devices'           : API_URL + "/v1/devices",
    'put_device_control'    : API_URL + "/v1/devices/control",
    'get_device_state'      : API_URL + "/v1/devices/state?",

}

class Govee:
    """Govee Device class
    WIP. Not currently using this yet."""

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
    devices = resp.json()['data']['devices']
    for device in devices:
        device['state'] = get_device_state(device)
    return devices

def get_avail_controls(device: dict):
    print(device['supportCmds'])


def power_device(device, cmd = "off") -> None:
    headers = {
        "Govee-API-Key": API['api_key'],
        "Content-Type": "application/json",
    }
    params = {
        'device'    : device['device'],
        'model'     : device['model'],
        'cmd'       : {
            'name': 'turn',
            'value': cmd
        }
    }
    resp = requests.put(API['put_device_control'], headers=headers, json=params)
    pass

def set_color(device: dict, red: int, green: int, blue: int) -> None:
    headers = {
        "Govee-API-Key": API['api_key'],
        "Content-Type": "application/json",
    }
    params = {
        'device'    : device['device'],
        'model'     : device['model'],
        'cmd'       : {
            'name': 'color',
            'value': {
                'r': red,
                'g': green,
                'b': blue
            }
        }
    }
    valid = [red, green, blue]
    for n in valid:
        if n < 0 or n > 255:
            print("Invalid input. Colors must be between 0-255")
            pass
    resp = requests.put(API['put_device_control'], headers=headers, json=params)
    pass

def set_temperature(device: dict, temperature: int) -> None:
    headers = {
        "Govee-API-Key": API['api_key'],
        "Content-Type": "application/json",
    }
    params = {
        'device'    : device['device'],
        'model'     : device['model'],
        'cmd'       : {
            'name': 'colorTem',
            'value': temperature
        }
    }
    resp = requests.put(API['put_device_control'], headers=headers, json=params)
    pass

def set_brightness(device: dict, brightness: int) -> None:
    headers = {
        "Govee-API-Key": API['api_key'],
        "Content-Type": "application/json",
    }
    params = {
        'device'    : device['device'],
        'model'     : device['model'],
        'cmd'       : {
            'name': 'brightness',
            'value': brightness
        }
    }
    resp = requests.put(API['put_device_control'], headers=headers, json=params)
    pass

def get_device_state(device) -> list:
    headers = {
        "Govee-API-Key": API['api_key'],
        "Content-Type": "application/json",
    }
    req_params = {
        'device'    : device['device'],
        'model'     : device['model'],
    }
    resp = requests.get(url=API['get_device_state'] + urlencode(req_params), headers=headers, json=req_params)
    resp.raise_for_status()
    return resp.json()['data']['properties']

def choose_colors() -> tuple[int, int, int]:
    try:
        red =    int(input("Red     > "))
        green =  int(input("Green   > "))
        blue =   int(input("Blue    > "))
    except:
        print("Must be integers")
        return 0, 0, 0
    return red, green, blue

def choose_number(min: int, max: int) -> int:
    try:
        choice =    int(input("Choose a number ({}-{}) > ".format(min, max)))
        if choice < min or choice > max:
                print("Invalid input. Minimum={}. Maximum={}".format(min, max))
                return min
    except:
        print("Must be integers")
        return min
    return choice

def menu_print() -> None:
    print("\n~ Govee API Controller ~")
    print("1. Get devices")
    print("2. Get device state")
    print("3. Show device state")
    print("4. Power ON")
    print("5. Power OFF")
    print("6. Set color")
    print("7. Set color temperature")
    print("8. Set brightness")
    print("0. Exit")

def main():
    # Get my devices
    devices = get_devices()
    # Grab the first (and only) device
    light_stick = devices[0]

    # Making a temporary menu for easier testing
    while True:
        menu_print()
        choice = str(input(">>> "))
        match choice:
            case '0':
                break
            case '1':
                devices = get_devices()
                light_stick = devices[0]
            case '2':
                light_stick['state'] = get_device_state(light_stick)
                print(light_stick['state'])
            case '3': # Show device state
                print(light_stick['state'])
                get_avail_controls(light_stick)
            case '4':
                power_device(light_stick, "on")
            case '5':
                power_device(light_stick, "off")
            case '6':
                r, g, b = choose_colors()
                set_color(light_stick, r, g, b)
            case '7':
                temp = choose_number(2000, 9000)
                set_temperature(light_stick, temp)
            case '8':
                brightness = choose_number(0, 100)
                set_brightness(light_stick, brightness)
            case other:
                print("Invalid choice")
            


if __name__ == '__main__':
    main()
