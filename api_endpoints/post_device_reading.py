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
    os.environ['app_table'] = 'temp-commissioning-tempCommissioningAppTable50B65A65-1R9OTTT5IVI5Y'

    body_1 = {
        "name": "ns.up.data.process",
        "time": "2023-03-27T04:44:35.382655582Z",
        "identifiers": [
            {
            "device_ids": {
                "device_id": "24e124713c241951",
                "application_ids": {
                    "application_id": "jarrodstestapp"
                },
                "dev_eui": "24E124713C241951",
                "join_eui": "24E124C0002A0001",
                "dev_addr": "260D2DCF"
            }
            }
        ],
        "data": {
            "@type": "type.googleapis.com/ttn.lorawan.v3.UplinkMessage",
            "raw_payload": "QM8tDSaA204AA4z4eB0=",
            "payload": {
            "m_hdr": {
                "m_type": "UNCONFIRMED_UP"
            },
            "mic": "jPh4HQ==",
            "mac_payload": {
                "f_hdr": {
                "dev_addr": "260D2DCF",
                "f_ctrl": {
                    "adr": True
                },
                "f_cnt": 20187
                },
                "frm_payload": "Aw==",
                "full_f_cnt": 20187
            }
            },
            "settings": {
            "data_rate": {
                "lora": {
                "bandwidth": 125000,
                "spreading_factor": 7,
                "coding_rate": "4/5"
                }
            },
            "frequency": "917200000",
            "timestamp": 1792666372,
            "time": "2023-03-27T04:44:34.788Z"
            },
            "rx_metadata": [
            {
                "gateway_ids": {
                "gateway_id": "eui-24e124fffef2428b",
                "eui": "24E124FFFEF2428B"
                },
                "time": "2023-03-27T04:44:34.788Z",
                "timestamp": 1792666372,
                "rssi": -70,
                "channel_rssi": -70,
                "snr": 14,
                "frequency_offset": "-999",
                "uplink_token": "CiIKIAoUZXVpLTI0ZTEyNGZmZmVmMjQyOGISCCThJP/+8kKLEITW59YGGgsIs76EoQYQpZ6yUiCgj/iZlrF+KgwIsr6EoQYQgNrf9wI=",
                "channel_index": 2,
                "gps_time": "2023-03-27T04:44:34.788Z",
                "received_at": "2023-03-27T04:44:35.163446180Z"
            }
            ],
            "received_at": "2023-03-27T04:44:35.173957158Z",
            "correlation_ids": [
            "gs:conn:01GW0417XXQ55RGXWQPDY6RDMH",
            "gs:up:host:01GW041866CBFGAN8M7X7X0C2D",
            "gs:uplink:01GWGP3QZ4YNVX0SEPCEBEBVX5",
            "ns:uplink:01GWGP3QZ5K4MHQZJZNZ9G2KRB",
            "rpc:/ttn.lorawan.v3.GsNs/HandleUplink:01GWGP3QZ54NCZRHHF10470XMY"
            ],
            "device_channel_index": 10,
            "consumed_airtime": "0.046336s"
        },
        "correlation_ids": [
            "gs:conn:01GW0417XXQ55RGXWQPDY6RDMH",
            "gs:up:host:01GW041866CBFGAN8M7X7X0C2D",
            "gs:uplink:01GWGP3QZ4YNVX0SEPCEBEBVX5",
            "ns:uplink:01GWGP3QZ5K4MHQZJZNZ9G2KRB",
            "rpc:/ttn.lorawan.v3.GsNs/HandleUplink:01GWGP3QZ54NCZRHHF10470XMY"
        ],
        "origin": "ip-10-102-5-83.ap-southeast-2.compute.internal",
        "context": {
            "tenant-id": "CgN0dG4="
        },
        "visibility": {
            "rights": [
            "RIGHT_APPLICATION_TRAFFIC_READ"
            ]
        },
        "unique_id": "01GWGP3R5P7SA50JH5Q6WN6WS2"
        }

    body = {
        'end_device_ids': {
            'device_id': 'tank-3-level', 
            'application_ids': {
                'application_id': 'jarrodstestapp'
            }, 
            'dev_eui': '24E124713C241806', 
            'join_eui': '24E124C0002A0001', 
            'dev_addr': '260DE2F5'
        }, 
        'correlation_ids': [
            'as:up:01GWG8ZQ7QSZ3XH0CJEFBVJEPW', 
            'gs:conn:01GW0417XXQ55RGXWQPDY6RDMH', 
            'gs:up:host:01GW041866CBFGAN8M7X7X0C2D', 
            'gs:uplink:01GWG8ZQ14XKQQHA641Q9X3X1E', 
            'ns:uplink:01GWG8ZQ15CZDSRZV3MNANCDW8', 
            'rpc:/ttn.lorawan.v3.GsNs/HandleUplink:01GWG8ZQ150CM8S4WVQ3C4C05K', 
            'rpc:/ttn.lorawan.v3.NsAs/HandleUplink:01GWG8ZQ7PGR8A9G4JZJXR7CKX'
        ], 
        'received_at': '2023-03-27T00:55:11.862537599Z', 
        'uplink_message': {
            'session_key_id': 'AYcgHGxyfXxELB++4I0EBw==', 
            'f_port': 85, 
            'f_cnt': 37, 
            'frm_payload': 'AXVkA4KgBQQAAA==', 
            'decoded_payload': {
                'battery': 100, 
                'distance': 1440, 
                'position': 'normal'
            }, 
            'rx_metadata': [
                {
                    'gateway_ids': {
                        'gateway_id': 'eui-24e124fffef2428b', 
                        'eui': '24E124FFFEF2428B'
                    }, 
                    'time': '2023-03-27T00:55:11.277Z', 
                    'timestamp': 914057384, 
                    'rssi': -70, 
                    'channel_rssi': -70, 
                    'snr': 13.5, 
                    'frequency_offset': '-846', 
                    'uplink_token': 'CiIKIAoUZXVpLTI0ZTEyNGZmZmVmMjQyOGISCCThJP/+8kKLEKjR7bMDGgwI79KDoQYQ7JWbtwIgwKDDkM2geyoMCO/Sg6EGEMDeioQB', 
                    'channel_index': 3, 
                    'gps_time': '2023-03-27T00:55:11.277Z', 
                    'received_at': '2023-03-27T00:55:11.643507359Z'
                }
            ], 
            'settings': {
                'data_rate': {
                    'lora': {
                        'bandwidth': 125000, 
                        'spreading_factor': 7, 
                        'coding_rate': '4/5'}
                    }, 
                    'frequency': '917400000', 
                    'timestamp': 914057384, 
                    'time': '2023-03-27T00:55:11.277Z'
                }, 
            'received_at': '2023-03-27T00:55:11.653833866Z', 
            'consumed_airtime': '0.061696s', 
            'network_ids': {
                'net_id': '000013', 
                'tenant_id': 'ttn', 
                'cluster_id': 'au1', 
                'cluster_address': 'au1.cloud.thethings.network'
                }
            }
        }

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