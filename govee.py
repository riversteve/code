# Govee API
# https://govee-public.s3.amazonaws.com/developer-docs/GoveeDeveloperAPIReference.pdf
# API v1.7

import sys
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

class Device:
    def __init__(self, device_info):
        """
        Initialize the Device class with information from the device_info dictionary.
        
        Args:
        - device_info (dict): A dictionary containing device details.
        """
        self.device_id = device_info.get('device', '')
        self.model = device_info.get('model', '')
        self.device_name = device_info.get('deviceName', '')
        self.controllable = device_info.get('controllable', False)
        self.retrievable = device_info.get('retrievable', False)
        self.support_cmds = device_info.get('supportCmds', [])
        self.state = {item_key: item_value for d in device_info.get('state', []) for item_key, item_value in d.items()}
        self.properties = device_info.get('properties', {})
        
    def get_state(self):
        """
        Returns the current state of the device.
        
        Returns:
        - state (dict): A dictionary representing the current state of the device.
        """
        headers = {
            "Govee-API-Key": API['api_key'],
            "Content-Type": "application/json",
        }
        req_params = {
            'device'    : self.device_id,
            'model'     : self.model,
        }
        try:
            resp = requests.get(url=API['get_device_state'] + urlencode(req_params), headers=headers)
            resp.raise_for_status()
            properties = resp.json()['data']['properties']
                        # Convert list of dictionaries into a single dictionary
            updated_state = {item_key: item_value for d in properties for item_key, item_value in d.items()}
            self.state = updated_state

        except requests.RequestException as e:
            print(f"Error fetching device state: {e}")
            # Handle the error or return an empty state / error state
            self.state = {}

        return self.state
    
    # Placeholder methods for device interaction
    def turn_on(self):
        return self._power_device("on")

    def turn_off(self):
        return self._power_device("off")
    
    def set_brightness(self, brightness):
        pass
    
    def set_color(self, r, g, b):
        return self._set_color(r, g, b)
    
    def update_state(self, new_state):
        """
        Updates the device's state based on the provided new_state dictionary.
        
        Args:
        - new_state (dict): A dictionary containing state updates.
        """
        self.state.update(new_state)

    def _modify_state(self, key, value):
        """
        Private method to modify a specific dictionary value within self.state.
        
        Args:
            - key (str): The key of the state item you want to update.
            - value : The new value for that key.
            
        Note: This is a private method and should only be used inside this class, as it does not follow Python's naming convention. In other classes or outside the current one, this method will not be accessible.
        """
        self.state[key] = value


    def _put_device_control(self, headers, params):
        try:
            resp = requests.put(API['put_device_control'], headers=headers, json=params)
            resp.raise_for_status()
            return True
        except:
            return False

    def _power_device(self, cmd):
        """
        Powers the device on or off.

        Args:
        - cmd (string): on or off.
        Returns True if successfully sent PUT request to API
        """
        headers = {
            "Govee-API-Key": API['api_key'],
            "Content-Type": "application/json",
        }
        params = {
            'device'    : self.device_id,
            'model'     : self.model,
            'cmd'       : {
                'name': 'turn',
                'value': cmd
            }
        }
        try:
            if cmd.lower() in ['on', 'off']:
                return self._put_device_control(headers, params)
        except requests.RequestException as e:
            print(f"Error fetching device state: {e}")
        return False
    
    def _set_color(self, red: int, green: int, blue: int) -> None:
        headers = {
            "Govee-API-Key": API['api_key'],
            "Content-Type": "application/json",
        }
        params = {
            'device'    : self.device_id,
            'model'     : self.model,
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
                return False
        return self._put_device_control(headers, params)
    
    def _set_brightness(self, brightness: int) -> None:
        headers = {
            "Govee-API-Key": API['api_key'],
            "Content-Type": "application/json",
        }
        params = {
            'device'    : self.device_id,
            'model'     : self.model,
            'cmd'       : {
                'name': 'brightness',
                'value': brightness
            }
        }
        return self._put_device_control(headers, params)



# Example usage (commented out)
# device_info = {
#     'device': '66:EB:3C:83:07:3F:1F:67',
#     'model': 'H6072',
#     'deviceName': 'floor lamp H6072',
#     'controllable': True,
#     'properties': {'colorTem': {'range': {'min': 2000, 'max': 9000}}},
#     'retrievable': True,
#     'supportCmds': ['turn', 'brightness', 'color', 'colorTem'],
#     'state': [{'online': True}, {'powerState': 'on'}, {'brightness': 100}, {'color': {'r': 255, 'b': 0, 'g': 255}}],
# }
# my_device = Device(device_info)
# print(my_device.get_state())

def get_devices() -> list:
    resp = requests.get(API['get_devices'], headers={"Govee-API-Key": API['api_key']})
    resp.raise_for_status()
    devices = resp.json()['data']['devices']
    for device in devices:
        device['state'] = get_device_state(device)
    return devices

def get_avail_controls(device: dict):
    print(device['supportCmds'])


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

    light = Device(devices[0])
    print(light.properties)
    print(type(light.properties))
    foo = light.properties
    print(foo)
    for k,v in foo.items():
        print (k, v, sep='\n')

    
    print(light.state)
    print(light.state['powerState'])
    if light.turn_off():
        print("Turned off the lights")
    time.sleep(3)
    light.get_state()
    print(light.state)
    time.sleep(2)
    if light.turn_on():
        print("Lights back on now")
    time.sleep(1)
    light.get_state()
    print(light.state)

    sys.exit(0)
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
            case _:
                print("Invalid choice")
            


if __name__ == '__main__':
    main()
