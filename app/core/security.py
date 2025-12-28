import hashlib
import json
import os
from typing import Tuple, Dict
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from app.core.config import get_settings

settings = get_settings()

class PhoneEncryptionService:
    def __init__(self):
        raw_keys = json.loads(settings.ENCRYPTION_ACTIVE_KEYS_JSON)
        self.keys: Dict[str, bytes] = {k: bytes.fromhex(v) for k, v in raw_keys.items()}
        self.current_key_id = settings.ENCRYPTION_CURRENT_KEY_ID

    def encrypt(self, plain_phone: str) -> Tuple[bytes, bytes, str]:
        if not plain_phone: raise ValueError("Empty phone")
        key = self.keys[self.current_key_id]
        iv = os.urandom(12)
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plain_phone.encode('utf-8')) + encryptor.finalize()
        return ciphertext + encryptor.tag, iv, self.current_key_id

    def decrypt(self, encrypted_blob: bytes, iv: bytes, key_id: str) -> str:
        key = self.keys[key_id]
        tag = encrypted_blob[-16:]
        ciphertext = encrypted_blob[:-16]
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
        decryptor = cipher.decryptor()
        return (decryptor.update(ciphertext) + decryptor.finalize()).decode('utf-8')

    @staticmethod
    def hash_for_search(plain_phone: str) -> str:
        return hashlib.sha256(plain_phone.strip().encode('utf-8')).hexdigest()

    @staticmethod
    def mask_phone(plain_phone: str) -> str:
        if len(plain_phone) < 7: return plain_phone
        return f"{plain_phone[:3]}****{plain_phone[-4:]}"

encryption_service = PhoneEncryptionService()
