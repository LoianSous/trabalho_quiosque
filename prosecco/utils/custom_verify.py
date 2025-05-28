from flask import abort, request
from flask_login import current_user, login_manager
from prosecco.config import User_type
from functools  import wraps

def access_required(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            
            if current_user.u_type == User_type.ADMIN:
                return f(*args, **kwargs)
            
            if current_user.u_type not in allowed_roles:
                abort(403)
                
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator


def ip_authorized_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)

        if current_user.u_type != User_type.ADMIN:
            client_ip = request.remote_addr
            allowed = any(
                device.ip == client_ip and device.a_state == Device_state.ACTIVE
                for device in current_user.devices
            )
            if not allowed:
                abort(403)
        return f(*args, **kwargs)
    return decorated_function