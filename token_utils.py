import hashlib
import jwt
import hashlib
from cryptography.fernet import Fernet

from string import ascii_uppercase, digits
from random import choice

SECRET_KEY = '52d3f853c19f8b63c0918c126422aa2d99b1aef33ec63d41dea4fadf19406e54'
PAYLOAD_KEY = b'OEXI_dPVFkL5Niy0MZA1ip9fzG8FVizYyuPU-VejwNw='
# key = Fernet.generate_key() para gerar uma nova Key


def encriptando_jwt(payload_dict):
    """ documentação: https://pyjwt.readthedocs.io/en/stable/"""

    return jwt.encode(
        payload_dict,
        SECRET_KEY,
        algorithm="HS256"
    )


def decriptando_jwt(jwt_payload):
    """ documentação: https://pyjwt.readthedocs.io/en/stable/"""

    return jwt.decode(
        jwt_payload,
        SECRET_KEY,
        algorithm="HS256"
    )


def create_custom_token():

    return ''.join([choice(ascii_uppercase + digits) for i in range(15)])


def encrypt_password(password):

    string_para_criptografar = password

    # Cria um objeto hash SHA-256
    hash_object = hashlib.sha256()

    # Atualiza o hash com a string a ser criptografada
    hash_object.update(string_para_criptografar.encode())

    # Obtém o hash resultante como uma string hexadecimal
    return hash_object.hexdigest()

def encrypt_message(mensagem, chave=PAYLOAD_KEY):
    """documentação: https://pypi.org/project/cryptography/
                     https://cryptography.io/en/latest/fernet/
    """

    cipher = Fernet(PAYLOAD_KEY)

    return (cipher.encrypt(str.encode(mensagem))).decode()

def dencrypt_message(mensagem, chave=PAYLOAD_KEY):

    cipher = Fernet(PAYLOAD_KEY)

    return cipher.decrypt(mensagem).decode()


# teste = encrypt_message("Lorem Ipsum Dollor")
# print(teste)

# teste = dencrypt_message(teste)
# print(f" ===== utro teste \n {teste}")


# payload = {
#         'userId': '55395427-265a-4166-ac93-da6879edb57a',
#         'exp': 1556841600,
#         'outro_teste': "tesssssste"}

# bs64_payload = encriptando_jwt(payload)

# print(bs64_payload)

# final_value = decriptando_jwt(bs64_payload)

# print(final_value)

# print(bool(payload == final_value))