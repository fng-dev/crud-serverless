from src.helpers.helpers import (
    response,
    getQueryString,
    getBody,
    validateRequest,
    traceback_details,
)
from src.models.User import User


def list(event, context):
    try:
        user = User()
        params = getQueryString(event)

        data = user.list(params)
        if "items" in data:
            return response(data)

        return response({"error": data["error"]}, 400)
    except BaseException as error:
        traceback_details_data = traceback_details()
        return response(
            {"error": "{}".format(error), "traceback": traceback_details_data}, 400
        )


def read(event, context):
    try:
        print(context)
        params = getQueryString(event)

        if "PK" not in params or "SK" not in params:
            return response({"error": "Ingresar pk y sk a la request"}, 400)

        user = User()
        data = user.read(params)

        if "item" in data:
            return response(data)

        return response({"error": data["error"]}, 400)
    except BaseException as error:
        traceback_details_data = traceback_details()
        return response(
            {"error": "{}".format(error), "traceback": traceback_details_data}, 400
        )


def create(event, context):
    try:
        user = User()
        errors = validateRequest(user.rules, getBody(event))

        if len(errors) != 0:
            return response({"errors": errors}, 400)

        data = user.create(getBody(event))

        if "error" in data:
            return response(data, 400)

        return response({"message": "Usuario creado con exito", "item": data})
    except BaseException as error:
        traceback_details_data = traceback_details()
        return response(
            {"error": "{}".format(error), "traceback": traceback_details_data}, 400
        )


def update(event, context):
    try:
        user = User()
        errors = validateRequest(user.rules, getBody(event))

        if len(errors) != 0:
            return response({"errors": errors}, 400)

        data = user.update(getBody(event))

        if data == False:
            return response({"message": "Usuario no encontrado", "item": None}, 400)

        return response(data)
    except BaseException as error:
        traceback_details_data = traceback_details()
        return response(
            {"error": "{}".format(error), "traceback": traceback_details_data}, 400
        )


def signin(event, context):
    try:
        body = getBody(event)
        user = User()
        signInResponse = user.signIn(body)

        if signInResponse == False:
            return response({"message": "Usuario no encontrado", "item": None}, 400)

        # Generate token
        return response({"message": "Sesion iniciada con exito", "item": None})

    except BaseException as error:
        traceback_details_data = traceback_details()
        return response(
            {"error": "{}".format(error), "traceback": traceback_details_data}, 400
        )
