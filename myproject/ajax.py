import json

from django.http import JsonResponse


def validate(request, id):
    with open('myproject/ajax_files/status.json', 'r') as jsonfile:
        data = json.load(jsonfile)
        jsonfile.close()
        return JsonResponse(data)
