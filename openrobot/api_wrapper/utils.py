import os
import json

def get_token_from_file():
    # OpenRobot-CLI uses this method for storing the tokens.
    # It gets it from ~/.openrobot/api/cridentials.json first.
    # If the token key or the file/folder can't be found, it will try to get the token from the OPENROBOT_API_TOKEN env.
    # If any of the above fails, it will return None.
    
    try:
        dir = os.path.expanduser("~/.openrobot")

        with open(f'{dir}/api/cridentials.json', 'r') as f:
            cridentials = json.load(f)

            token = cridentials['token']
    except:
        token = os.environ.get('OPENROBOT_API_TOKEN')

    return token