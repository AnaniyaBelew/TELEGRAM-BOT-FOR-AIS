import requests
import json
from prettytable import PrettyTable
data={'username':"anteneh",'password':'anteneh'}
logged_in=False
def get_bearer(username,password):
    api_url = "http://ais.blackneb.com/api/token/"
    payload = {
        "username": username,
        "password": password
    }
    try:
        response = requests.post(api_url, data=payload)
        response.raise_for_status()  # Raise an exception if the request was not successful
        return response.text  # Return the response from the API
    except requests.exceptions.RequestException as e:
        # Handle any errors that occurred during the request
        print(f"An error occurred: {e}")
        return None
def login_access(username,password,tok):
    api_url = "http://ais.blackneb.com/api/ais/login"
    headers= {
     "Authorization": f"Bearer {tok}",
}
    payload = {
        "username": username,
        "password": password
    }
    try:
        response = requests.post(api_url, headers=headers,data=payload)
        response.raise_for_status()  # Raise an exception if the request was not successful
        return response.text  # Return the response from the API
    except requests.exceptions.RequestException as e:
        # Handle any errors that occurred during the request
        print(f"An error occurred: {e}")
        return None
def get_claims(id):
    api_url = "http://ais.blackneb.com/api/ais/getclaimsbot"
    payload = {
        "proposerID": id,
    }
    try:
        response = requests.post(api_url,data=payload)
        response.raise_for_status()  # Raise an exception if the request was not successful
        return response.text  # Return the response from the API
    except requests.exceptions.RequestException as e:
        # Handle any errors that occurred during the request
        print(f"An error occurred: {e}")
        return None
def print_dict_as_table(dictionary):
    table = PrettyTable(dictionary.keys())
    table.add_row(dictionary.values())
    print(table)
def divide_dict(dictionary, keys):
    dict1 = {key: dictionary[key] for key in keys if key in dictionary}
    dict2 = {key: dictionary[key] for key in dictionary if key not in keys}
    return dict1, dict2
resp_auth=get_bearer(data['username'],data['password'])
newresp=json.loads(resp_auth)
ref=newresp['refresh']
acc=newresp['access']
resp_acc=login_access(data['username'],data['password'],str(acc))
newresp_acc=json.loads(resp_acc)
stat=newresp_acc[0]
#logged_in=True
if logged_in:
    getresp=json.loads(get_claims(stat['proposerID']))
    claim=getresp[0]
    keys_to_divide = ['id', 'proposer', 'accident_id','created_at','vehicle']

    dict1, dict2 = divide_dict(claim, keys_to_divide)
    print_dict_as_table(dict1)
    print_dict_as_table(dict2)
else:
    print("fail")



