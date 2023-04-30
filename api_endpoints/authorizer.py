import os
from Shared.errors import ClientError, NotFoundError, ServerError
from Shared.api import API
from Shared.auth import Authorizer
import json 

def main(event):
    try:
        arn = event['methodArn']
        method_arn = "{}".format(str(arn).split('/')[0])
        Auth = Authorizer(access_table=os.environ['ACCESS_TABLE'], endpoint_arn=method_arn)
        auth = Auth._check_token(token=event['authorizationToken'])
    except Exception as e:
        auth = "Deny"
    auth_response = Auth.build_response(auth = auth)
    return auth_response

def handler(event, context):
    try:
        response = main(event)        
        return API.response(
            code = 200, 
            body = json.dumps(response) 
        )
    except ClientError as e:
        return API.response(
            code = 400, 
            body = json.dumps({"Error": f"{e}"}) 
        )
    except NotFoundError as e:
        return API.response(
            code = 404, 
            body = json.dumps({"Error": f"{e}"}) 
        )
    except ServerError as e:
        return API.response(
            code = 500, 
            body = json.dumps({"Error": f"{e}"}) 
        )
    except Exception as e:
        return API.response(
            code = 500, 
            body = json.dumps({"Error": f"{e}"}) 
        )

if __name__ == "__main__":
    os.environ["some_env_var"] = "env_var_value"

    body = {
        "attribute1": "value1",
        "attribute2": "value2",
    }

    event = {
        'httpMethod': 'GET',
        'resource': '/example',
        'queryStringParameters': {},
        'pathParameters': {},
        'body' : json.dumps(body)
    }

    handler(event, context=None)