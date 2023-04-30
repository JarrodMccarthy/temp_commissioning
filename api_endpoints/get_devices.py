import json
import os
from Shared.errors import handle_error_response
from Shared.api import API
from Shared.dynamo import Dynamo


def main(event):
    """ The end point handles taking a device reading and putting it into Dynamo DB"""

    payload = API.parse_payload(event)
    print(f"PAYLOAD: {payload}")

    dynamo = Dynamo(table_name=os.environ['app_table'])

    devices = dynamo.get_items(column_name="PK", column_value="type#device")

    result = {
        "devices": devices
    }

    return result

@handle_error_response
def handler(event, context=None):
    return main(event)
        
    
if __name__ == "__main__":
    os.environ['app_table'] = 'temp-commissioning-tempCommissioningAppTable50B65A65-1R9OTTT5IVI5Y'

    event = {
        'httpMethod': 'GET',
        'resource': '/device',
        'queryStringParameters': {
        },
        'pathParameters': {},
    }

    resp = handler(event, context=None)
    print(resp)