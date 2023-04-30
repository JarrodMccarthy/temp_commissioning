from uuid import uuid4
from datetime import datetime
from typing import Dict, Any, Union
from Shared.dynamo import Dynamo

class Measurement:
    def __init__(self, 
                device_id: str,
                metric: str,
                value: float,
                units: str,
                record_type: str = "type#measurement", 
                ) -> None:
        self.record_type = record_type
        self.measurement_id = f"metric#{metric}-ts#{datetime.now()}"
        self.record_ts_id = f"{device_id}-{self.measurement_id}"
        self.metric = metric
        self.value = value
        self.units = units
    
    def to_dynamo_object(self):
        device_dict = vars(self)
        new_dict = {}
        mapping = {
            "record_type": "PK",
            "record_ts_id": "SK"
        }
        for key, value in device_dict.items():
            if mapping.get(key):
                new_dict[mapping[key]] = value
            else:
                new_dict[key] = value
        return new_dict

class TempDevice:
    def __init__(self, 
                record_type: str = "type#device", 
                name: str = None,
            ) -> None:
        self.record_type = record_type
        self.name = name

class EM310UDL(TempDevice):
    def __init__(self, 
                dev_eui: str,
                record_type: str = "type#device", 
                name: str = None,
            ) -> None:
        super().__init__(record_type, name)
        self.record_ts_id = f"deviceid-{dev_eui}"
        self.dev_eui = dev_eui
        self.device_id = dev_eui
        self.metric_unit_map = {
            "battery": "%",
            "distance": "mm",
            "position": ""
        }

    def post_measurement(self, body: dict, dynamo: Dynamo):
        measurements = body["uplink_message"]['decoded_payload']
        i = 0
        for metric, value in measurements.items():
            device_id = self.record_ts_id
            units = self.metric_unit_map.get(metric)
            measurement = Measurement(device_id, metric, str(value), units)
            put_measurement = dynamo.put_item(measurement.to_dynamo_object())
            if put_measurement['ResponseMetadata']['HTTPStatusCode'] == 200:
                i += 1
        return {"added": f"{i}-measurements"}

    def check_existence(self, dynamo: Dynamo) -> bool:
        device_records = dynamo.get_items(column_name="PK", column_value="type#device")

        for device in device_records: 
            if device["dev_eui"] == self.dev_eui:
                return True
        return False
    
    def decode_payload(self, raw_payload) -> dict:
        return {}


    def to_dynamo_object(self):
        device_dict = vars(self)
        new_dict = {}
        mapping = {
            "record_type": "PK",
            "record_ts_id": "SK"
        }
        for key, value in device_dict.items():
            if mapping.get(key):
                new_dict[mapping[key]] = value
            else:
                new_dict[key] = value
        return new_dict


