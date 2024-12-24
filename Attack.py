import string
import random
from Tree.Models.Encoder import Encoder

def generate_random_string(length):
    """Generate a random string of given length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def check_file_collisions():
    """Check for collisions between the files"""
    file_names = ["Attack Files/file1.txt", 'Attack Files/file2.txt', 'Attack Files/file3.txt', 
                  'Attack Files/file4.txt', 'Attack Files/file5.txt']
    
    # Store hashes for each file
    file_hashes = {}
    
    print("\n=== Checking for collisions between files ===")
    for file_name in file_names:
        encoder = Encoder(file_name, isFile=True)
        current_hash = encoder.getFinalHash()
        
        # Check if this hash already exists
        if current_hash in file_hashes:
            print(f"\nCOLLISION FOUND!")
            print(f"File 1: {file_hashes[current_hash]}")
            print(f"File 2: {file_name}")
            print(f"Hash: {current_hash}")
            return True
        
        file_hashes[current_hash] = file_name
        print(f"Hash for {file_name}: {current_hash}")
    
    print("\nNo collisions found between files.")
    return False

def check_random_string_collisions():
    """Check for collisions using random strings"""
    max_attempts = 10000
    test_file = "Attack Files/file1.txt"  # Using first file as reference
    
    print("\n=== Checking for collisions with random strings ===")
    print(f"Will try {max_attempts} random strings...")
    
    # Get original hash
    encoder = Encoder(test_file, isFile=True)
    original_hash = encoder.getFinalHash()
    original_data = encoder.getOriginalData()
    
    # Try random strings
    for i in range(max_attempts):
        candidate_data = generate_random_string(len(original_data))
        encoder = Encoder(candidate_data, isFile=False)
        candidate_hash = encoder.getFinalHash()
        
        if candidate_hash == original_hash and candidate_data != original_data:
            print(f"\nCOLLISION FOUND after {i+1} attempts!")
            print(f"Original data hash: {original_hash}")
            print(f"Colliding string: {candidate_data}")
            return True
        
        if (i + 1) % 1000 == 0:
            print(f"Tried {i + 1} strings...")
    
    print("\nNo collisions found with random strings.")
    return False

def main():
    print("Starting collision detection...")
    
    # First check file collisions
    file_collision = check_file_collisions()
    
    # Then check random string collisions
    random_collision = check_random_string_collisions()
    
    # Summary
    print("\n=== SUMMARY ===")
    print(f"File Collisions Found: {'Yes' if file_collision else 'No'}")
    print(f"Random String Collisions Found: {'Yes' if random_collision else 'No'}")

if __name__ == "__main__":
    main()