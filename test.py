import unittest
import os
from database import Database
from signature import generate_signature, verify_signature
from Tree.Models.Encoder import Encoder

class TestAuthentication(unittest.TestCase):
    def setUp(self):
        # Initialize test database
        self.db = Database()
        # Test user credentials
        self.test_username = "testuser"
        self.test_password = "Test123!"

    def tearDown(self):
        # Properly close the database connection
        self.db.__del__()  # This calls the close() method
        # Clean up by removing test database
        if os.path.exists('users.db'):
            try:
                os.remove('users.db')
            except PermissionError:
                # If file is still locked, wait a moment and try again
                import time
                time.sleep(0.1)
                os.remove('users.db')

    def test_user_registration(self):
        # Test successful registration
        self.assertTrue(self.db.add_user(self.test_username, self.test_password))
        # Test duplicate registration
        self.assertFalse(self.db.add_user(self.test_username, self.test_password))

    def test_user_authentication(self):
        # Register a test user first
        self.db.add_user(self.test_username, self.test_password)
        
        # Test valid credentials
        self.assertTrue(self.db.verify_user(self.test_username, self.test_password))
        # Test invalid password
        self.assertFalse(self.db.verify_user(self.test_username, "wrongpassword"))
        # Test non-existent user
        self.assertFalse(self.db.verify_user("nonexistent", self.test_password))

class TestDigitalSignature(unittest.TestCase):
    def setUp(self):
        self.test_data = "Test message for digital signature"
        self.encoder = Encoder(self.test_data, isFile=False)
        self.root_hash = self.encoder.getFinalHash()

    def test_signature_generation(self):
        # Test signature generation
        signature = generate_signature(self.root_hash)
        self.assertIsNotNone(signature)
        self.assertIsInstance(signature, bytes)

    def test_signature_verification(self):
        # Generate a signature
        signature = generate_signature(self.root_hash)
        
        # Test valid signature verification
        self.assertTrue(verify_signature(self.root_hash, signature))
        
        # Test invalid data verification
        modified_data = "Modified " + self.test_data
        modified_encoder = Encoder(modified_data, isFile=False)
        modified_hash = modified_encoder.getFinalHash()
        self.assertFalse(verify_signature(modified_hash, signature))

    def test_tampered_signature(self):
        # Generate a signature
        signature = generate_signature(self.root_hash)
        
        # Tamper with the signature
        tampered_signature = bytearray(signature)
        tampered_signature[0] = (tampered_signature[0] + 1) % 256
        
        # Verify should fail with tampered signature
        self.assertFalse(verify_signature(self.root_hash, bytes(tampered_signature)))

    def test_empty_data_signature(self):
        # Test signing empty data
        empty_encoder = Encoder("", isFile=False)
        empty_hash = empty_encoder.getFinalHash()
        signature = generate_signature(empty_hash)
        self.assertTrue(verify_signature(empty_hash, signature))

    def test_large_data_signature(self):
        # Test signing large data
        large_data = "x" * 1000000  # 1MB of data
        large_encoder = Encoder(large_data, isFile=False)
        large_hash = large_encoder.getFinalHash()
        signature = generate_signature(large_hash)
        self.assertTrue(verify_signature(large_hash, signature))

class TestMerkleTree(unittest.TestCase):
    def setUp(self):
        self.test_data = "The quick brown fox jumps over the lazy dog"
        self.encoder = Encoder(self.test_data, isFile=False)

    def test_hash_consistency(self):
        # Test if same input produces same hash
        encoder2 = Encoder(self.test_data, isFile=False)
        self.assertEqual(self.encoder.getFinalHash(), encoder2.getFinalHash())

    def test_hash_difference(self):
        # Test if different inputs produce different hashes
        modified_data = self.test_data + " modified"
        modified_encoder = Encoder(modified_data, isFile=False)
        self.assertNotEqual(self.encoder.getFinalHash(), modified_encoder.getFinalHash())

    def test_file_processing(self):
        # Create a temporary test file
        test_file_path = "test_file.txt"
        with open(test_file_path, "w") as f:
            f.write(self.test_data)

        try:
            # Test file-based encoding
            file_encoder = Encoder(test_file_path, isFile=True)
            self.assertIsNotNone(file_encoder.getFinalHash())
        finally:
            # Clean up
            if os.path.exists(test_file_path):
                os.remove(test_file_path)

    def test_special_characters(self):
        # Test data with special characters
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        special_encoder = Encoder(special_chars, isFile=False)
        self.assertIsNotNone(special_encoder.getFinalHash())

    def test_unicode_characters(self):
        # Test data with unicode characters
        unicode_data = "Hello 世界! ñ á é í ó ú"
        unicode_encoder = Encoder(unicode_data, isFile=False)
        self.assertIsNotNone(unicode_encoder.getFinalHash())

    def test_large_file_processing(self):
        # Test processing a large file
        large_file_path = "large_test_file.txt"
        try:
            with open(large_file_path, "w") as f:
                f.write("x" * 1000000)  # 1MB of data

            large_file_encoder = Encoder(large_file_path, isFile=True)
            self.assertIsNotNone(large_file_encoder.getFinalHash())
        finally:
            if os.path.exists(large_file_path):
                os.remove(large_file_path)

    def test_empty_file(self):
        # Test processing an empty file
        empty_file_path = "empty_test_file.txt"
        try:
            with open(empty_file_path, "w") as f:
                f.write("")

            empty_file_encoder = Encoder(empty_file_path, isFile=True)
            self.assertIsNotNone(empty_file_encoder.getFinalHash())
        finally:
            if os.path.exists(empty_file_path):
                os.remove(empty_file_path)

if __name__ == "__main__":
    unittest.main()
