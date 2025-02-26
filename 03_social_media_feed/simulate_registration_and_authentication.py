from passlib.context import CryptContext

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to hash a plain text password
def get_hashed_password(plain_password):
    return pwd_ctx.hash(plain_password)

# Function to verify a password against a hashed password
def verify_password(plain_password, hashed_password):
    print("Verifying hash:", hashed_password, "Length:", len(hashed_password))
    return pwd_ctx.verify(plain_password, hashed_password)

# Simulate user registration
plain = "secret123"
hashed = get_hashed_password(plain)
print("Generated hash:", hashed)

# Simulate user authentication
if verify_password("secret123", hashed):
    print("Password is correct!")
else:
    print("Invalid password!")

