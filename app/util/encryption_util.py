import hashlib
from typing import Dict

import jwt


class Encryption:
    with open("app/lib/secret/private_key.txt", "rb") as private:
        private_key = private.read()
    with open("app/lib/secret/public_key.txt", "rb") as public:
        public_key = public.read()

    @staticmethod
    def md5_encryption(text: str) -> str:

        return str(hashlib.md5(bytes(text, encoding="utf8")).hexdigest())


    @classmethod
    def jwt_encode(cls, data: Dict) -> str:
        return jwt.encode(payload=data, key=cls.private_key, algorithm="RS256")


    @classmethod
    def jwt_decode(cls, text: str) -> Dict or bool:
        try:
            data = jwt.decode(text, cls.public_key, algorithms=["RS256"])
            return data
        except:
            return False

# print(Encryption.md5_encryption("superxx"))
