import bcrypt
def _hash_password(password):
        """
           Hash a password 
        """
        password = password.encode('utf-8')
        return bcrypt.hashpw(password, salt=bcrypt.gensalt())