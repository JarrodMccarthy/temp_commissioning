import boto3

class Dynamo:
    def __init__(self, table_name: str) -> None:
        ddb = boto3.resource('dynamodb')
        self.table = ddb.Table(table_name)

    def _build_update_expression(self, params: dict):
        '''Constructs the update expression
        Input of params = { 'att1': 'val1', 'att2': 'val2' }
        becomes
            update_expression = 'set #att1 = :att1, #att2 = :att2'
            update_names = { '#att1': 'att1', '#att2': 'att2' }
            update_values = { ':att1': 'val1', ':att2': 'val2' }
            
        returned as (update_expression, update_names, update_values)
        '''
        update_names = dict()
        update_values = dict()
        update_expression = ["set "]
        
        for key,val in params.items():
            update_names[f"#{key}"] = key # To avoid 'reserved word' conflicts
            update_values[f":{key}"] = val # To avoid 'reserved word' conflicts
            update_expression.append(f" #{key} = :{key},")
        
        return "".join(update_expression)[:-1], update_names, update_values
    
    def get_items(self, column_name: str, column_value: str, index_name: str = None) -> list:
        if index_name:
            items = self.table.query(
                IndexName=index_name,
                KeyConditionExpression=f"#{column_name}=:{column_name}",
                ExpressionAttributeValues={
                    f':{column_name}': f'{column_value}',
                },
                ExpressionAttributeNames= { f"#{column_name}": f"{column_name}" }
            ).get('Items')
        else:
            items = self.table.query(
                #IndexName=index_name,
                KeyConditionExpression=f"#{column_name}=:{column_name}",
                ExpressionAttributeValues={
                    f':{column_name}': f'{column_value}',
                },
                ExpressionAttributeNames= { f"#{column_name}": f"{column_name}" }
            ).get('Items')
        return items

    def get_items_begins_with(self, pk_name: str, pk_value: str, sk_name: str, sk_value: str, index_name: str = None, sort_ascending: bool = True) -> list:
        if index_name:
            items = self.table.query(
                IndexName=index_name,
                KeyConditionExpression=f"#{pk_name}=:{pk_name} AND begins_with ({sk_name}, :{sk_name})",
                ExpressionAttributeValues={
                    f':{pk_name}': f'{pk_value}',
                    f':{sk_name}': f'{sk_value}',
                },
                ExpressionAttributeNames= { f"#{pk_name}": f"{pk_name}", f"#{sk_name}": f"{sk_name}" },
                ScanIndexForward=sort_ascending,
            ).get('Items')
        else:
            items = self.table.query(
                #IndexName=index_name,
                KeyConditionExpression=f"#{pk_name}=:{pk_name} AND begins_with (#{sk_name}, :{sk_name})",
                ExpressionAttributeValues={
                    f':{pk_name}': f'{pk_value}',
                    f':{sk_name}': f'{sk_value}',
                },
                ExpressionAttributeNames= { f"#{pk_name}": f"{pk_name}", f"#{sk_name}": f"{sk_name}" },
                ScanIndexForward=sort_ascending,
            ).get('Items')
        return items

    def put_item(self, item: dict):
        return self.table.put_item(Item=item)
    
    def update_item(self, column_name: str, column_value: str, attributes: dict):
        update_expression, update_names, update_values = self._build_update_expression(attributes)
        r = self.table.update_item(
            Key={
                f'{column_name}': f'{column_value}',
            },
            UpdateExpression=update_expression,
            ExpressionAttributeNames=update_names,
            ExpressionAttributeValues=update_values,
            ConditionExpression=f'attribute_exists({column_name})'
        )
        if 'error' in r:
            raise Exception(f"Error: Failed to update item {column_name}")
        return r