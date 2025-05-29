from flask_login import current_user
from functools import wraps
from flask import abort

def somente_advogado(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if current_user.papel not in ['advogado', 'administrador']:
            abort(403)
        return f(*args, **kwargs)
    return wrapper

def somente_admin(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if current_user.papel != 'administrador':
            abort(403)
        return f(*args, **kwargs)
    return wrapper