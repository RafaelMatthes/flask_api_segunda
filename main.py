from flask import Flask, request

import json

from exceptions import UserNotAllowedError
from classes import UserManager, TokenManager

app = Flask(__name__)

@app.route('/api/signup', methods=['POST'])
def create_new_user():
    user_manager = UserManager()

    request_data = json.loads(request.data)

    username = request_data.get('username')
    password = request_data.get('password')

    new_user = {
        "username": username if username else None,
        "password": password if password else None,
    }

    user_manager.add_new_user(**new_user)

    return {}, 201


@app.route('/api/login', methods=['POST'])
def create_or_get_token():

    try:
        user_manager = UserManager()
        request_data = json.loads(request.data)

        new_user = {
            "username": request_data.get('username'),
            "password": request_data.get('password'),
        }

        token = user_manager.get_user_token(**new_user)

        return {"Authorization": f"Token {token}"}, 200

    except UserNotAllowedError as err:
        return {"error": str(err)}, 401

    except Exception as err:
        return {"error": str(err)}, 500


@app.route('/api/valid_token', methods=['POST'])
def valid_token():

    try:
        request_data = json.loads(request.data)

        token = request_data.get('token')
        token_manager = TokenManager()
        user_data = token_manager.verify_token(token_code=token)

        return {"user": user_data }, 200

    except UserNotAllowedError as err:
        return {"error": str(err)}, 401

    except json.JSONDecodeError as err:
        return {"error": str(err)}, 400


app.run(host='0.0.0.0', port=5000)