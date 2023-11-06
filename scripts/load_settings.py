import json
import os



def load_settings(pi):
    os.chdir('../settings')
    with open("pi_settings" + pi + ".json", 'r', buffering=100) as file:
        return json.load(file)

