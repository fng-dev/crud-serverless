import logging
import boto3

class DynamoDB:
    def __init__(self, model):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        self.dynamodbTableName = "GuxMainTable"
        self.dynamodb = boto3.resource("dynamodb")
        self.table = self.dynamodb.Table(self.dynamodbTableName)
        self.model = model
        
    def getTable(self):
        return self.table
    
    def getLogger(self):
        return self.logger