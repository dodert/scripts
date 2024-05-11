import requests, json, os
from dotenv import dotenv_values

API_KEY = ""
BASE_URL = ""
COMMON_HEDERS = {}

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def change_working_directory():
    print (f"Current working directory: '{os.getcwd()}'")
    
    filePath = os.path.dirname(os.path.realpath(__file__))
    
    print(f"Script path: '{filePath}'")
    
    os.chdir(filePath)
    
    print (f"working directory after change it: '{os.getcwd()}'")

def load_variables():

    global API_KEY, BASE_URL, COMMON_HEDERS

    secrets = dotenv_values(".env")

    API_KEY = secrets["API_KEY"]
    BASE_URL = secrets["BASE_URL"]
    COMMON_HEDERS = {'Content-Type': 'application/json', 'x-api-key': API_KEY}

def get_person_assets(personId):
    url = f"{BASE_URL}/api/person/{personId}/assets"
    headers = COMMON_HEDERS
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError(f"Failed to fetch assets. Status code: {response.status_code}, Response text: {response.text}")

def add_assets_to_album(album_id, asset_ids, key=None):
    def show_result():
        totalItems = len(respjson)
        duplicates = [elemento for elemento in respjson if not elemento['success'] and elemento['error'] == 'duplicate']
        success = [elemento for elemento in respjson if elemento['success']]

        print(f'\t\t{bcolors.OKCYAN}Result: {bcolors.BOLD}{len(success)}{bcolors.ENDC}{bcolors.OKCYAN} added and {bcolors.BOLD}{len(duplicates)}{bcolors.ENDC}{bcolors.OKCYAN} duplicated of {bcolors.BOLD}{totalItems}{bcolors.ENDC}{bcolors.OKCYAN}. {bcolors.OKGREEN}OK!!!')

    url = f"{BASE_URL}/api/album/{album_id}/assets"
    payload = json.dumps({"ids": asset_ids})
    params = {'key': key} if key else {}

    response = requests.put(url, headers=COMMON_HEDERS, data=payload, params=params)
    
    if response.status_code == 200:
        respjson = response.json()
        
        show_result()

        return respjson
    else:
        raise ValueError(f"Failed to add assets. Status code: {response.status_code}, Response text: {response.text}")

def main():    
    person_id = "f9d2f802-f06f-45e0-a071-503b2ca5627b"
    album_id = "3fceaef6-c1db-4f1a-afbe-3548f86ac88e"
    
    try:

        change_working_directory()
        load_variables()

        assets = get_person_assets(person_id)

        unique_asset_ids = set()

        for asset in assets:
            unique_asset_ids.add(asset['id'])

        asset_ids_list = list(unique_asset_ids)

        add_assets_to_album(album_id, asset_ids_list)
        
    except Exception as e:
        if hasattr(e, 'message'):
            print(e.message)

if __name__ == "__main__":
    main()