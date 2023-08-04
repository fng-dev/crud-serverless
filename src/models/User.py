import boto3
from boto3.dynamodb.conditions import Key
import uuid
import json
from src.models.Model import DynamoDB
from src.helpers.security import Security 


class User(DynamoDB):
    def __init__(self):
        self.PK = "USER#"
        self.SK = "EMAIL#"
        self.fillable = [
            "name",
            "email",
            "address",
            "year",
            "info",
            "password",
            "created_at",
            "udpated_at",
        ]
        self.upgradeable = ["name", "address", "year", "info"]
        self.hidden = ["password"]
        self.rules = [
            "name",
            "email",
            "address",
            "year",
            "password",
        ]
        self.limit = 10
        super().__init__("User")

    def list(self, params=None):
        try:
            if params != None and "limit" in params:
                self.setLimit(int(params["limit"]))

            body = {
                "IndexName": "Model",
                "KeyConditionExpression": Key("GS1PK").eq("USER"),
                "Limit": self.limit,
            }

            if "nextPage" in params:
                body["ExclusiveStartKey"] = json.loads(params["nextPage"])

            response = self.table.query(**body)
            items = self.mutateData(response["Items"])

            result = {
                "message": "Usuarios listados con exito",
                "items": items,
                "total": len(items),
            }

            if "LastEvaluatedKey" in response:
                result["nextPage"] = response["LastEvaluatedKey"]

            return result

        except BaseException as error:
            self.logger.exception("No fue posible cargar los usuarios")
            return {"error": "{}".format(error)}

    def read(self, payload):
        try:
            response = self.table.get_item(
                Key={
                    "PK": "{}{}".format(self.PK, payload["PK"]),
                    "SK": "{}{}".format(self.SK, payload["SK"]),
                }
            )

            if "Item" in response:
                item = self.mutateData(response["Item"])
                result = {"message": "Usuario listado con exito", "item": item}
                return result

            return {"error": "Usuario no encontrado"}

        except BaseException as error:
            self.logger.exception("No fue posible encontrar este usuario")
            return {"error": "{}".format(error)}

    def create(self, payload):
        try:
            isAvailable = self.isMailAvailable(payload["email"])

            if isAvailable == False:
                return {"error": "Este email ya no esta disponible"}

            validFields = {}

            for field in payload.keys():
                if field in self.fillable:
                    validFields[field] = payload[field]

            validFields["PK"] = "{}{}".format(self.PK, uuid.uuid4().hex)
            validFields["SK"] = "{}{}".format(self.SK, payload["email"])
            validFields["GS1PK"] = "USER"
            
            security = Security()
            validFields["password"] = security.hash_password(validFields["password"])
            response = self.table.put_item(Item=validFields)

            return response
        except BaseException as error:
            self._logger.exception("No fue posible agregar este usuario")
            return {"error": "{}".format(error)}

    def update(self, payload):
        try:
            response = self.table.get_item(
                Key={
                    "PK": "{}{}".format(self.PK, payload["PK"]),
                    "SK": "{}{}".format(self.SK, payload["SK"]),
                }
            )

            if "Item" in response:
                item = response["Item"]
                for field in payload.keys():
                    if field in self.upgradeable:
                        item[field] = payload[field]

                self.table.put_item(Item=item)
                result = {"message": "Usuario actualizado con exito", "item": item}
                return result

            return False
        except BaseException as error:
            self.logger.exception("No fue posible actualizar este usuario")
            return {"error": "{}".format(error)}
        
    def signIn(self, payload):
        response = self.table.query(
            IndexName="Model",
            KeyConditionExpression=Key("GS1PK").eq("USER")
            & Key("SK").eq("{}{}".format(self.SK, payload["email"])),
        )
        
        if len(response["Items"]) != 0:
            user = response["Items"][0]
            security = Security()
            if "password" not in user:
                return False
            singInResponse = security.login(payload["password"], user["password"].value)
            return singInResponse
            
        return False

    def mutateData(self, payload):
        if isinstance(payload, (list)):
            for item in payload:
                item["PK"] = item["PK"].split("#")[1]
                item["SK"] = item["SK"].split("#")[1]
                for prop in self.hidden:
                    if prop in item:
                        del item[prop]
            return payload

        payload["PK"] = payload["PK"].split("#")[1]
        payload["SK"] = payload["SK"].split("#")[1]
        for prop in self.hidden:
                    if prop in payload:
                        del payload[prop]
        return payload

    def isMailAvailable(self, email):
        response = self.table.query(
            IndexName="Model",
            KeyConditionExpression=Key("GS1PK").eq("USER")
            & Key("SK").eq("{}{}".format(self.SK, email)),
        )

        if len(response["Items"]) != 0:
            return False

        return True

    def setLimit(self, limit):
        self.limit = limit
