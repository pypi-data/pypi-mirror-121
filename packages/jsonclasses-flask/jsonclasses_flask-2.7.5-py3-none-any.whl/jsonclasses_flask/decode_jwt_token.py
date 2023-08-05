from flask import current_app
from jsonclasses.jobject import JObject
from jwt import decode


def decode_jwt_token(token: str) -> JObject:
    key = current_app.config['jsonclasses_encode_key']
    id = decode(token, key, algorithms=['HS256'])['operator']
    cls = current_app.config['jsonclasses_operator_cls']
    return cls.id(id).exec()

