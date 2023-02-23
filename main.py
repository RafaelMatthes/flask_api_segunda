from flask import Flask, request

import json

from exceptions import UserNotAllowedError


app = Flask(__name__)

from classes import UserManager


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

        token = user_manager.get_or_create_token(**new_user)

        return {"Authorization": f"Token {token}"}, 200

    except UserNotAllowedError as err:
        return {"error": str(err)}, 401

    except Exception as err:
        return {"error": str(err)}, 500


app.run()

# TODO: criar uma tabela para armazenar o Token e a data de criação para cada usuário

# TODO: Criar um método para criar um token jwt ou recuperar um token quando informado username e password

# TODO: Criar um endpoint para verificar se o token informado existe na base de dados e se a data de criação
# do token tem mais de 2 dias ( datime.today() - created_at )
# se a data de criação for maior que 2 dias, retornar 401, senão 200