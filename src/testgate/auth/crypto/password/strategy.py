from .pbkdf2 import Pbkdf2
from .scrypt import Scrypt
from .abstract import PasswordHashStrategy

pbkdf2 = Pbkdf2()
scrypt = Scrypt()


class Pbkdf2PasswordHashStrategy(PasswordHashStrategy):

    def encode(self, password: str, salt: str) -> bytes:
        return pbkdf2.encode(password=password, salt=salt)

    def verify(self, password: str, encoded_password: bytes) -> bool:
        return pbkdf2.verify(password=password, encoded_password=encoded_password)


class ScryptPasswordHashStrategy(PasswordHashStrategy):

    def encode(self, password: str, salt: str) -> bytes:
        return scrypt.encode(password=password, salt=salt)

    def verify(self, password: str, encoded_password: bytes) -> bool:
        return scrypt.verify(password=password, encoded_password=encoded_password)
