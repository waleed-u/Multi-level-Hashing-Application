if __name__ == "__main__":
    # Initialize the handler
    handler = DigitalSignature()

    # Sample data
    data = "This is a sample Merkle Tree root hash."

    # Generate signature
    signature = handler.generate_signature(data)
    print(f"Generated Signature: {signature}")

    # Verify signature
    is_valid = handler.verify_signature(data, signature)
    print(f"Signature Valid: {is_valid}")

    # Export public key
    public_key = handler.export_public_key()
    print(f"Public Key:\n{public_key}")
