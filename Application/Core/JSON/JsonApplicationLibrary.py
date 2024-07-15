import requests
import config_file
import json
import Core.JSON.JsonLibrary as JsonLibrary


def GetWorkersRequest():
    url = config_file.host_link + '/jsonapi/node/rabotnik'  # Пример URL для GET запроса

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return [response.status_code, data]
    else:
        print("Ошибка при выполнении GET запроса")
        print(f"Статус код ошибки: {response.status_code}")
        print(f"Текст ошибки: {response.text}")


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
    response = config_file.session.post(url, json=body, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print(data)
        config_file.csrf_token = str(JsonLibrary.find_variables_by_name(data, 'csrf_token')[0])

    else:
        print("Ошибка при выполнении POST запроса:")
        print(f"Статус код ошибки: {response.status_code}")
        print(f"Текст ошибки: {response.text}")


def PostNewWorker(new_worker):
    url = config_file.host_link + '/jsonapi/node/rabotnik'

    body = new_worker.DeserializeJSON()

    headers = {
        'Content-Type': 'application/vnd.api+json',
        'X-CSRF-Token': str(config_file.csrf_token)
    }
    print(str(headers))

    response = config_file.session.post(url, json=body, headers=headers)

    if response.status_code == 201:
        new_post = response.json()
        print("Новый рабочий создан:")
        print(new_post)
    else:
        print("Ошибка при выполнении POST запроса:")
        print(f"Статус код ошибки: {response.status_code}")
        print(f"Текст ошибки: {response.text}")


def DeleteWorker(delete_worker):
    url = config_file.host_link + '/jsonapi/node/rabotnik/' + delete_worker.id

    headers = {
        'X-CSRF-Token': str(config_file.csrf_token)
    }
    response = config_file.session.delete(url, headers=headers)

    if response.status_code == 204:
        print("Sucsess delete")
    else:
        print("Ошибка при выполнении DELETE запроса:")
        print(f"Статус код ошибки: {response.status_code}")
        print(f"Текст ошибки: {response.text}")


def PatchWorker(patch_worker):
    url = config_file.host_link + '/jsonapi/node/rabotnik/' + patch_worker.id
    body = patch_worker.DeserializePatchJSON()

    headers = {
        'Content-Type': 'application/vnd.api+json',
        'X-CSRF-Token': str(config_file.csrf_token)
    }
    response = config_file.session.patch(url, json=body, headers=headers)

    if response.status_code == 200:
        print("Sucsess patch")
    else:
        print("Ошибка при выполнении Patch запроса:")
        print(f"Статус код ошибки: {response.status_code}")
        print(f"Текст ошибки: {response.text}")


def GetAllPodrazdelenieOptions():
    url = config_file.host_link + '/jsonapi/taxonomy_term/tip_podrazdeleniya'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return [response.status_code, data]
    else:
        print("Ошибка при выполнении GET запроса")
        print(f"Статус код ошибки: {response.status_code}")
        print(f"Текст ошибки: {response.text}")



def GetAllPodrazdelenieOptionNames():
    data = GetAllPodrazdelenieOptions()
    if data[0] == 200:
        s = []
        for json_entity in data[1]['data']:
            name = JsonLibrary.find_variables_by_name(json_entity, "name")
            name = str(name)[2:]
            name = name[:(len(name)-2)]
            s.append(name)
        return s
    else:
        return ["None"]
