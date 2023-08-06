from typing import List

from boto3.dynamodb.conditions import Key
from lib.aws_utils import get_dynamo_table


def _get_table(table_id):
    return get_dynamo_table(table_id)


def save_item(table_id: str, item: dict) -> dict:
    table = _get_table(table_id=table_id)
    return table.put_item(Item=item)


def query_table_by_id(table_id: str, id: str) -> List[dict]:
    table = _get_table(table_id=table_id)
    response = table.query(KeyConditionExpression=Key('id').eq(id))
    return response['Items']


def scan_table(table_id: str):
    table = _get_table(table_id=table_id)
    response = table.scan()
    return response['Items']


class DynamoDBDAO:

    def __init__(self, **kwargs):
        self.table_id = kwargs.get("table_id")

    def save_item(self, item: dict):
        return save_item(table_id=self.table_id, item=item)

    def query_by_id(self, id: str):
        return query_table_by_id(table_id=self.table_id, id=id)

    def scan(self):
        return scan_table(table_id=self.table_id)
