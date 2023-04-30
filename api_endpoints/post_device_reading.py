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

    dev_eui=payload["body"]["end_device_ids"]["dev_eui"]
    name=payload["body"]["end_device_ids"]["device_id"]

    dynamo = Dynamo(table_name=os.environ['app_table'])

    current_device = EM310UDL(dev_eui=dev_eui, name=name)

    dynamo.put_item(current_device.to_dynamo_object())

    put_measurement_result = current_device.post_measurement(payload["body"], dynamo)

    return put_measurement_result

@handle_error_response
def handler(event, context=None):
    return main(event)
        
    
if __name__ == "__main__":
    os.environ['app_table'] = 'apptable-name'

    body = {}

    event = {
        'httpMethod': 'POST',
        'resource': '/device',
        'queryStringParameters': {
        },
        'pathParameters': {},
        'body' : json.dumps(body)
    }

    resp = handler(event, context=None)
    print(resp)