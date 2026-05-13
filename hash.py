from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password):
    return generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

if __name__ == "__main__":
    password = input("Enter a password to hash: ")
    hashed_password = hash_password(password)
    print(f"Hashed password: {hashed_password}")

    # Test the hashed password
    password_to_check = input("Enter the password to check: ")
    if check_password_hash(hashed_password, password_to_check):
        print("Password is correct!")
    else:
        print("Password is incorrect!")