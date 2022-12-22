import json

from auth.models import Token
from authlib.jose import jwk
from fastapi import Request
from datetime import timedelta, datetime, timezone
from auth.settings import PUBLIC_KEY_PATH, PRIVATE_KEY_PATH
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import jwt
import hashlib
import base64


def get_private_key():
    with open(PRIVATE_KEY_PATH, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    return private_key


def get_public_key():
    with open(PUBLIC_KEY_PATH, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    return public_key


def create_access_token(
        username: str,
        roles: list[str],
        expires_delta: int = 300
) -> Token:
    dt_now = datetime.now(tz=timezone.utc)
    expire_at = dt_now + timedelta(seconds=expires_delta)
    secret_key = get_private_key()
    encoded_jwt = jwt.encode(
        {
            "sub": username,
            "exp": expire_at,
            "iat": dt_now,
            "roles": roles,
        },
        key=secret_key,
        algorithm="RS256",
        headers={
            "kid": "cHVibGljLWtleS1pZA"
        }
    )
    return Token(access_token=encoded_jwt)


def decode_token(token: str):
    secret_key = get_public_key()
    decoded = jwt.decode(
        token,
        key=secret_key,
        algorithms=["RS256"],
    )
    return decoded


def generate_jwk() -> dict:
    key = get_public_key()
    key_data = jwk.dumps(key, kty='RSA')
    return {
        "kid": "cHVibGljLWtleS1pZA",
        "alg": "RS256",
        "kty": "RSA",
        "use": "sig",
        "n": key_data["n"],
        "e": key_data["e"],
    }


def get_jwk_fingerprint() -> str:
    jwk = generate_jwk()
    jwk_str = json.dumps({"e": jwk["e"], "kty": jwk["kty"], "n": jwk["n"]})
    jwk_encoded = hashlib.sha256(jwk_str.encode('utf-8')).digest()
    return base64.urlsafe_b64encode(jwk_encoded).decode('utf-8')
