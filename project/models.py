from flask import abort, session
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or not session.get('is_admin'):
            abort(403)  # Forbidden
        return f(*args, **kwargs)
    return decorated_function