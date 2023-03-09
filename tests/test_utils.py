# https://pythonbasics.org/flask-sqlalchemy/#:~:text=Step%201%20%2D%20Install%20the%20Flask%2DSQLAlchemy%20extension.&text=Step%202%20%2D%20You%20need%20to,SQLAlchemy%20class%20from%20this%20module.&text=Step%203%20%2D%20Now%20create%20a,for%20the%20database%20to%20use.&text=Step%204%20%2D%20then%20use%20the,an%20object%20of%20class%20SQLAlchemy.

from token_utils import encriptando_jwt


def test_encrypte_jwt():

    data = {
        "value": "teste",
        "value2": "teste2",
    }

    encripted_payload = encriptando_jwt(
        payload_dict=data,

    )
    print(encripted_payload)

    assert encripted_payload != data

