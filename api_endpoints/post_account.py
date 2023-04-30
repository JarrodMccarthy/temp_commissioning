import json
import os
from Shared.errors import ClientError, NotFoundError, ServerError
from Shared.api import API
from Shared.cognito import Cognito
from Shared.dynamo import Dynamo
from Shared.account import User, Role, Account

def main(event):
    """This endpoint is the sign up end point
    create account and first admin user"""
    payload = API.parse_payload(event)
    account = Account()
    user_pool = Cognito(pool_id=os.environ['userpool_id'], client_id = os.environ['client_id'])
    dynamo = Dynamo(table_name=os.environ['user_table'])

    role = Role(role=0) # 0 is admin
    admin_user = User(
        account = account,
        role = role,
        first = payload["body"]["first"],
        last = payload["body"]["last"],
        nickname = payload["body"]["nickname"],
        email = payload["body"]["email"],
        password = payload["body"]["password"],
        )

    # create Admin user in Cognito
    sign_up_result = user_pool.sign_up(admin_user) # working 

    # create account in dynamo
    dynamo.put_item(vars(account))

    # create admin user in dynamo
    dynamo.put_item(vars(admin_user))

    result = dict(
        auth = sign_up_result.get('AuthenticationResult'),
        account_id = account.record_ts_id,
        username = admin_user.nickname,
        first = admin_user.first,
        last = admin_user.last,
        role = admin_user.role
    )

    return result


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
    os.environ['userpool_id'] = "userpool-id"
    os.environ['client_id'] = "userpool-clientid"
    os.environ['user_table'] = 'user-table'

    body = {
        "first": "fakefirst",
        "last": "fakelast",
        "nickname": "fakenickname",
        "email": "jarrodmccarthy12@gmail.com",
        "password": "fakep@ssword1234",
        "role": 0
    }

    event = {
        'httpMethod': 'POST',
        'resource': '/auth/account',
        'queryStringParameters': {
            "account_id": ""
        },
        'pathParameters': {},
        'body' : json.dumps(body)
    }

    resp = handler(event, context=None)
    print(resp)