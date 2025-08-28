import os
import json
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class CredentialManager:
    """Manages encryption, decryption, and storage of osu! API credentials"""

    def __init__(self):
        self.config_file = "data/config.json"

    def _derive_key(self, osu_user_id: str, salt: bytes) -> bytes:
        """Derive encryption key from osu user ID and salt"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100_000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(osu_user_id.encode()))
        return key

    def encrypt_credentials(
        self, osu_user_id: str, client_id: str, client_secret: str
    ) -> dict:
        """Encrypt client credentials using osu user ID as key"""
        # Generate random salt for this encryption
        salt = os.urandom(32)
        key = self._derive_key(osu_user_id, salt)
        fernet = Fernet(key)

        encrypted_client_id = fernet.encrypt(client_id.encode()).decode()
        encrypted_client_secret = fernet.encrypt(client_secret.encode()).decode()

        return {
            "ecid": encrypted_client_id,
            "ecsec": encrypted_client_secret,
            "salt": base64.urlsafe_b64encode(salt).decode(),
        }

    def decrypt_credentials(self, osu_user_id: str) -> dict:
        """Decrypt stored credentials"""
        if not self.credentials_exist():
            return None

        with open(self.config_file, "r") as f:
            data = json.load(f)

        if "salt" not in data:
            raise ValueError(
                "Salt not found in config file, delete data/config.json and run again"
            )
        else:
            salt = base64.urlsafe_b64decode(data["salt"].encode())

        key = self._derive_key(osu_user_id, salt)
        fernet = Fernet(key)

        try:
            client_id = fernet.decrypt(data["ecid"].encode()).decode()
            client_secret = fernet.decrypt(data["ecsec"].encode()).decode()

            return {
                "osu_user_id": osu_user_id,
                "client_id": client_id,
                "client_secret": client_secret,
            }
        except Exception:
            return None

    def save_credentials(self, encrypted_data: dict):
        """Save encrypted credentials to file"""
        # check if data dir exists, if not create it
        if not os.path.exists("data"):
            os.makedirs("data")

        with open(self.config_file, "w") as f:
            json.dump(encrypted_data, f, indent=2)

    def credentials_exist(self) -> bool:
        """Check if credentials file exists"""
        return os.path.exists(self.config_file)
