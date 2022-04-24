import random, string
import bcrypt
from utils import logger
import jwt

def generate_random_string():
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=16)) + "-" + ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    return random_string

def generate_hash_from(string_to_hash):
    try:
        string_to_hash = str(string_to_hash).encode("UTF-8")
        hashed_string = bcrypt.hashpw(string_to_hash, salt=bcrypt.gensalt(12))
        return hashed_string
    except Exception as error:
        logger.error("generate_hash", "generate_hash", str(error))
        return None

def generate_jwt(user_info):
    try:
        encoded = jwt.encode(user_info, key="secret", algorithm="HS256")
        if not encoded:
            raise Exception("Error while generating jwt")
        return encoded
    except Exception as error:
        logger.error("auth_user", "generate_jwt", str(error))
        return None

def decode_jwt(token):
    try:
        decoded = jwt.decode(token, key="secret", algorithms=["HS256"])
        return decoded
    except Exception as error:
        logger.error("UserAuth", "decode_jwt", str(error))
        return {}