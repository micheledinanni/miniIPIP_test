import json
from .logger import logger_file
from django.http import JsonResponse


def validate(request, id):
    try:
        with open('myproject/ajax_files/status.json', 'r') as jsonfile:
            data = json.load(jsonfile)
            jsonfile.close()
            return JsonResponse(data)
    except Exception as e:
        error = str(e)
        logger_file(error)
