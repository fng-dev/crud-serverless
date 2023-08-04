import bcrypt

class Security:
    def hash_password(self, password):
        pwd_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(pwd_bytes, salt)
    
    def login(self, password, hash):
        pwd_bytes = password.encode("utf-8")
        return bcrypt.checkpw(pwd_bytes, hash)