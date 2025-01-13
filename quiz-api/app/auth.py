from app.jwt_utils import decode_token
from flask import request, jsonify

def authenticate():
    # Vérifier le token d'authentification
    token = request.headers.get('Authorization')

    if not token or not token.startswith("Bearer "):
        return jsonify({"error": "Token manquant ou invalide"}), 401

    token = token.split(" ")[1]  # Extraire uniquement le token JWT

    # Décoder le token
    try:
        decode_token(token)
    except Exception as e:
        return jsonify({"error": str(e)}), 401
