import json
import os
from Shared.errors import handle_error_response
from Shared.api import API
from Shared.dynamo import Dynamo
from Shared.temp_device import EM310UDL
import base64

def decoder(measurement):
    return measurement

def main(event):
    """ The end point handles taking a device reading and putting it into Dynamo DB"""

    payload = API.parse_payload(event)
    print(f"PAYLOAD: {payload}")

    deviceid = payload["queryStringParameters"]["deviceid"]
    metric = payload["queryStringParameters"]["metric"]

    sk_value = "deviceid-" + deviceid + "-metric#" + metric

    dynamo = Dynamo(table_name=os.environ['app_table'])

    latest_measurements = dynamo.get_items_begins_with(pk_name="PK", pk_value="type#measurement", sk_name="SK", sk_value=sk_value, sort_ascending=False)

    result = {
        "measurements": latest_measurements
    }

    return result

@handle_error_response
def handler(event, context=None):
    return main(event)
        
    
if __name__ == "__main__":
    os.environ['app_table'] = 'apptable-name'

    event = {
        'httpMethod': 'GET',
        'resource': '/device',
        'queryStringParameters': {
            "deviceid": "24E124713C241806",
            "metric": "battery"
        },
        'pathParameters': {},
    }

    resp = handler(event, context=None)
    print(resp)