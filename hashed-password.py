# hash_password.py

# from passlib.context import CryptContext

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def hash_password(password: str):
#     return pwd_context.hash(password)

# if __name__ == "__main__":
#     password = input("Enter admin password: ")
#     print("Hashed Password:", hash_password(password))


# import bcrypt

# # Original password (for example, 'admin password')
# password = b'eE9OnSygIreDzQO'

# # Hash generated previously
# hashed_password = b'$2b$12$coB1LgDifTCk6mZrt5JwEepKo89WdKwNuu8Y7utXL6nymutBzgg2e'

# # Check if the password matches the hash
# if bcrypt.checkpw(password, hashed_password):
#     print("Password matches")
# else:
#     print("Password does not match")
