import requests
import json
import time
import threading


# Define the pulse sending URL
url = ""

# Heartbeat control variable
variable_parameter = True


# 0
def setUrl(url_):
    '''
    ----------------------------------------------------------
    Function to set a URL for pulse sending

    Parameters:
        url_ (str): URL for pulse sending
    ----------------------------------------------------------
    '''

    global url
    url = url_


# 1
def sendPulse(name, description, additional_info, show_response):
    '''
    ----------------------------------------------------------
    Function to send a pulse to the server

    Parameters:
        name (str): process name
        description (str): process description
        additional_info (str) (optional): additional process data
        show_response (bool) (optional): show server response
    ----------------------------------------------------------
    '''

    try:
        payload = json.dumps({
            "processName": f"{name}",
            "processDescription": f"{description}",
            "additionalData": f"{additional_info}"
        })
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", url, headers=headers, data=payload)

    except Exception as e:
        print('\nError sending pulse! ', e)

    finally:
        try:
            if show_response:
                print(f'Heartbeat response: {response.status_code}')
            pass
        except:
            pass 


# 2
def pulse(interval, name, description, additional_info, show_response):
    '''
    ----------------------------------------------------------
    Function to send a pulse to the server at regular intervals

    Parameters:
        interval (int): time between pulses (in seconds)
        name (str): process name
        description (str): process description
        additional_info (str) (optional): additional process data
        show_response (bool) (optional): show server response
    ----------------------------------------------------------
    '''

    while variable_parameter:
        sendPulse(name, description, additional_info, show_response)
        time.sleep(interval)


# 3
def heartbeat(interval = 600, name = '', description = '', additional_info = '', show_response = False):
    '''
    ----------------------------------------------------------
    Function to start the heartbeat

    Parameters:
        interval (int): time between pulses (in seconds)
        name (str): process name
        description (str): process description
        additional_info (str) (optional): additional process data
        show_response (bool) (optional): show server response
    ----------------------------------------------------------
    '''

    try:
        pulse_thread = threading.Thread(target=pulse, args=(interval, name, description, additional_info, show_response))
        pulse_thread.start()

    except Exception as e:
        print('Error in heartbeat thread! ', e)


# 4
def killHeartbeat():
    '''
    ----------------------------------------------------------
    Function to stop the heartbeat
    ----------------------------------------------------------
    '''

    global variable_parameter
    variable_parameter = not variable_parameter
