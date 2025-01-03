from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import utils
import os

class DigitalSignature:
    def __init__(self):
        """
        Initialize the DigitalSignature object and load the key pair from files.
        """
        self.private_key = None
        self.public_key = None
        self.load_keys()

    def load_keys(self):
        """
        Load keys from files. If files don't exist, generate new keys.
        """
        try:
            # Load private key
            with open('private_key.pem', 'rb') as f:
                private_pem = f.read()
                self.private_key = serialization.load_pem_private_key(
                    private_pem,
                    password=None
                )

            # Load public key
            with open('public_key.pem', 'rb') as f:
                public_pem = f.read()
                self.public_key = serialization.load_pem_public_key(
                    public_pem
                )
        except FileNotFoundError:
            # If keys don't exist, generate new ones
            self.private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048
            )
            self.public_key = self.private_key.public_key()

    def generate_signature(self, data: str) -> bytes:
        """
        Generate a digital signature for the provided data using the private key.
        
        Args:
            data (str): The data to sign.
        
        Returns:
            bytes: The generated digital signature.
        """
        signature = self.private_key.sign(
            data.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature

    def verify_signature(self, data: str, signature: bytes) -> bool:
        """
        Verify the digital signature using the public key.
        
        Args:
            data (str): The original data.
            signature (bytes): The digital signature to verify.
        
        Returns:
            bool: True if the signature is valid, False otherwise.
        """
        try:
            self.public_key.verify(
                signature,
                data.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False

    def export_public_key(self) -> str:
        """
        Export the public key in PEM format for sharing or storage.
        
        Returns:
            str: The PEM-formatted public key as a string.
        """
        pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return pem.decode()


# Expose reusable functions for the application
signature_handler = DigitalSignature()

def generate_signature(data: str) -> bytes:
    """
    Generate a digital signature for the given data using the handler.
    
    Args:
        data (str): The data to sign.
    
    Returns:
        bytes: The generated digital signature.
    """
    return signature_handler.generate_signature(data)

def verify_signature(data: str, signature: bytes) -> bool:
    """
    Verify the digital signature for the given data using the handler.
    
    Args:
        data (str): The original data.
        signature (bytes): The signature to verify.
    
    Returns:
        bool: True if valid, False otherwise.
    """
    return signature_handler.verify_signature(data, signature)
