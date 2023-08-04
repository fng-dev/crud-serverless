import json
import sys


def response(data, code=200, custonType="application/json"):
    return {
        "statusCode": code,
        "headers": {
            "Content-Type": custonType,
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
        },
        "body": json.dumps(data, default=str),
    }


def getQueryString(event):
    if "queryStringParameters" not in event:
        return {}

    return event["queryStringParameters"]


def getBody(event):
    try:
        data = json.loads(event["body"])
        return data
    except BaseException as error:
        return "An exception occurred: {}".format(error)


def validateRequest(fields, payload):
    errors = []
    for field in fields:
        if field not in payload:
            errors.append("El campo {} es obligatorio".format(field))

    return errors


def traceback_details():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback_details = {
        "filename": exc_traceback.tb_frame.f_code.co_filename,
        "lineno": exc_traceback.tb_lineno,
        "name": exc_traceback.tb_frame.f_code.co_name,
        "type": exc_type.__name__,
    }
    return traceback_details
