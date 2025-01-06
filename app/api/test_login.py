import bcrypt


def test_hash_pwd():
    pwd = "admin"
    salt = bcrypt.gensalt(rounds=10)
    hashed = bcrypt.hashpw(pwd.encode(), salt)
    print()
    print(str(hashed))

    pwd2 = "$2b$10$N7BBNuufRl3x1/ie4K3R5ebcRMjr5JWI9s7nmvbUPyPbrg2kUiM7i"
    print()
    print(str(pwd2.encode()))

    print(bcrypt.checkpw(pwd.encode(), pwd2.encode()))

