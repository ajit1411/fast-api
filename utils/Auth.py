from utils.helper import decode_jwt
from utils import logger

class UserAuth:
    def __init__(self, token = None):
        self._token = token
    
    @property
    def token(self):
        return self._token

    def decode(self):
        try:
            if not self.token:
                raise Exception("Token not found")
            token = str(self._token).split("Bearer ")[1]
            decoded = decode_jwt(token)
            return decoded
        except Exception as error:
            logger.error("UserAuth", "_decode", str(error))
            return None