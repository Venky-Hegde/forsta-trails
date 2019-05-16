from itsdangerous import URLSafeSerializer

from smartrec.settings import base


def generate_secretkey(email):
    s = URLSafeSerializer(base.SECRET_KEY)
    secretkey = s.dumps(email,salt=base.SALT)
    return secretkey


def authenticate_key(secretkey):
    s = URLSafeSerializer(base.SECRET_KEY)
    try:
        return s.loads(secretkey,salt=base.SALT)
    except:
        return False