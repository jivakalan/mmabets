import secrets

# Generate a random 64-character hexadecimal key (256 bits)
jwt_secret_key = secrets.token_hex(32)
print(jwt_secret_key)


##env variable updated