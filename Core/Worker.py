import Core.JSON.JsonLibrary as JsonLibrary
import json


class UWorker:
    def __init__(self, name="NoName", email="", country="None", work_position="None",podrazdelenie = 'None', id = "None"):
        self.name = name
        self.email = email
        self.country = country
        self.work_position = work_position
        self.podrazdelenie = podrazdelenie
        self.id = id

    def SerializeJSON(self, json):
        self.name = str(JsonLibrary.find_variables_by_name(json, 'title')[0])
        self.id = str(JsonLibrary.find_variables_by_name(json, 'id')[0])
        self.email = str(JsonLibrary.find_variables_by_name(json, 'field_pochta')[0])
        self.country = str(JsonLibrary.find_variables_by_name(json,'field_strana')[0])
        self.podrazdelenie = str(JsonLibrary.find_variables_by_name(json,'field_podrazdelenie')[0])

    def DeserializeJSON(self):
        reader = open("BaseWorkerExample.txt", "r+")
        body = json.loads(reader.read())
        JsonLibrary.replace_variables_by_name(body, "title", self.name)
        JsonLibrary.replace_variables_by_name(body, 'field_pochta', self.email)
        JsonLibrary.replace_variables_by_name(body, 'field_strana', self.country, 0)
        JsonLibrary.replace_variables_by_name(body, 'field_podrazdelenie', self.podrazdelenie)
        return body
