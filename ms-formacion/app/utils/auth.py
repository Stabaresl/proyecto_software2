from functools import wraps
from flask import request, jsonify
import jwt
import os

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            parts = request.headers['Authorization'].split(' ')
            if len(parts) == 2 and parts[0] == 'Bearer':
                token = parts[1]

        if not token:
            return jsonify({'success': False, 'message': 'Token no proporcionado.'}), 401

        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            request.auth_user_id   = payload.get('sub')
            request.auth_user_role = payload.get('role')
        except jwt.ExpiredSignatureError:
            return jsonify({'success': False, 'message': 'Token expirado.'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'success': False, 'message': 'Token inválido.'}), 401

        return f(*args, **kwargs)
    return decorated


def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if request.auth_user_role not in roles:
                return jsonify({'success': False, 'message': 'No tienes permiso para realizar esta acción.'}), 403
            return f(*args, **kwargs)
        return decorated
    return decorator