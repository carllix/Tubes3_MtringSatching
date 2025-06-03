# src/utils/encryption.py (Bonus Implementation)
import hashlib
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class SimpleEncryption:
    """Simple encryption utility for applicant data"""
    
    def __init__(self, password: str = None):
        if password is None:
            password = "ats_default_key_2024"  # Default key (not secure for production)
        
        self.password = password.encode()
        self.salt = b'salt_1234567890'  # Fixed salt (not secure for production)
        
    def _get_key(self):
        """Generate encryption key from password"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.password))
        return key
    
    def encrypt(self, data: str) -> str:
        """Encrypt string data"""
        if not data:
            return ""
        
        try:
            key = self._get_key()
            f = Fernet(key)
            encrypted_data = f.encrypt(data.encode())
            return base64.urlsafe_b64encode(encrypted_data).decode()
        except Exception as e:
            print(f"Encryption error: {e}")
            return data  # Return original data if encryption fails
    
    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt string data"""
        if not encrypted_data:
            return ""
        
        try:
            key = self._get_key()
            f = Fernet(key)
            decoded_data = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted_data = f.decrypt(decoded_data)
            return decrypted_data.decode()
        except Exception as e:
            print(f"Decryption error: {e}")
            return encrypted_data  # Return original data if decryption fails

class HashEncryption:
    """Hash-based encryption (one-way) for sensitive data"""
    
    @staticmethod
    def hash_data(data: str, salt: str = None) -> str:
        """Create hash of data with optional salt"""
        if salt is None:
            salt = "ats_salt_2024"
        
        combined = f"{data}{salt}"
        return hashlib.sha256(combined.encode()).hexdigest()
    
    @staticmethod
    def verify_hash(data: str, hashed_data: str, salt: str = None) -> bool:
        """Verify data against hash"""
        return HashEncryption.hash_data(data, salt) == hashed_data