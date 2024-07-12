import requests
import config_file
import json
from Core.JSON import JsonLibrary


def GetWorkersRequest():
    url = config_file.host_link + '/jsonapi/node/rabotnik'  # Пример URL для GET запроса

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        for x in data['data']:
            print(x)
    else:
        print("Ошибка при выполнении GET запроса")


def LoginOnDrupal():
    config_file.session = requests.Session()
    url = config_file.host_link + "/user/login"
    username = 'Oleg'
    password = '12099021qQ!!'

    body = {
        "name": "Oleg",
        "pass": "12099021qQ!!!"
    }
    params = {
        '_format': 'json'
    }

    headers = {
        'Content-Type': 'application/vnd.api+json'
    }
    response = config_file.session.post(url, json = body,params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print(data)
        config_file.csrf_token = str(JsonLibrary.find_variables_by_name(data, 'csrf_token')[0])

    else:
        print("Ошибка при выполнении POST запроса:")
        print(f"Статус код ошибки: {response.status_code}")
        print(f"Текст ошибки: {response.text}")


def PostNewWorker():
    url = config_file.host_link + '/jsonapi/node/rabotnik'

    reader = open("BaseWorkerExample.txt", "r+")
    body = json.loads(reader.read())
    JsonLibrary.replace_variables_by_name(body, "title", "Test Example")

    headers = {
        'Content-Type': 'application/vnd.api+json',
        'X-CSRF-Token': str(config_file.csrf_token)
    }
    print(str(headers))

    response = config_file.session.post(url, json=body, headers=headers)

    if response.status_code == 201:
        new_post = response.json()
        print("Новый пост создан:")
        print(new_post)
    else:
        print("Ошибка при выполнении POST запроса:")
        print(f"Статус код ошибки: {response.status_code}")
        print(f"Текст ошибки: {response.text}")

GetWorkersRequest()