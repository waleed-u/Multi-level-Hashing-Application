from signature import verify_signature
import binascii

def perform_replay_attack():
    with open('sign.txt', 'r') as f:
        captured_signature = f.read().strip()
    
    signature_bytes = bytes.fromhex(captured_signature)
    print(captured_signature)
    with open('file1.txt', 'r') as f:
        original_message = f.read()
    print(original_message)
    is_valid = verify_signature(original_message, captured_signature)
    print(is_valid)
    print(f"Replay Attack Result: {'Successful' if is_valid else 'Failed'}")
    return is_valid

if __name__ == "__main__":
    perform_replay_attack() 