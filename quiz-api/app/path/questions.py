from flask import Blueprint, request, jsonify
from app.jwt_utils import build_token, decode_token
from app.auth import authenticate
from app.questions_services import add_question_to_db, delete_question_by_position_from_db, delete_all_questions_from_db, update_question_in_db,get_quiz_info_from_db, get_all_questions_from_db, get_question_by_position_from_db
import hashlib
from app.models import get_db_connection
from flask_cors import cross_origin


# Créer un Blueprint pour les routes
bp = Blueprint('quiz', __name__)

# 2 - Flask creation
@bp.route('/')
@cross_origin(origin='*')  # Permet toutes les origines

def hello_world():
    x = 'world'
    return f"Hello, {x}"

# 3 - Get Quiz
@bp.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
    try:
        info = get_quiz_info_from_db()
        return jsonify(info), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



# 4 - Authentification
@bp.route('/login', methods=['POST'])
@cross_origin(origin='*')  # Permet toutes les origines
def post_login():
    try:
        payload = request.get_json()

        if "password" not in payload:
            return jsonify({"error": "Le champ 'password' est manquant"}), 400

        tried_password = payload["password"].encode('utf-8')
        hashed = hashlib.md5(tried_password).digest()

        if hashed == b'\xd8\x17\x06PG\x92\x93\xc1.\x02\x01\xe5\xfd\xf4_@':
            token = build_token()
            return jsonify({"token": token}), 200

        else:
            return jsonify({"error": "Mauvais mot de passe"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 5 - Add question (avec authentification)
@bp.route('/questions', methods=['POST'])
@cross_origin(origin='*')  # Permet toutes les origines
def add_question():
    try:
        authenticate()

        payload = request.get_json()

        # Vérification des champs requis
        if not all(key in payload for key in ['title', 'text', 'image', 'position', 'possibleAnswers']):
            return jsonify({"error": "Champs manquants"}), 400

        # Extraire les données
        title = payload['title']
        text = payload['text']
        image = payload['image']
        position = payload['position']
        possible_answers = payload['possibleAnswers']

        # Appeler la fonction du service pour ajouter la question
        question_id = add_question_to_db(title, text, image, position, possible_answers)

        # Retourner l'ID de la question créée
        return jsonify({"id": question_id}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    



# 6 - Delete question
@bp.route('/questions/<int:position>', methods=['DELETE'])
@cross_origin(origin='*')  # Permet toutes les origines
def delete_question(position):
    try:
        authenticate()

        # Appeler la fonction pour supprimer la question à la position donnée
        delete_question_by_position_from_db(position)

        return jsonify({"message": f"Question à la position {position} supprimée avec succès"}), 204

    except Exception as e:
        return jsonify({"error": str(e)}), 500




# 7 - Delete all questions
@bp.route('/questions/all', methods=['DELETE'])
@cross_origin(origin='*')  # Permet toutes les origines
def delete_all_questions():
    try:
        authenticate()

        # Appeler la fonction du service pour supprimer toutes les questions
        delete_all_questions_from_db()

        return jsonify({"message": "Toutes les questions ont été supprimées avec succès"}), 204

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

    try:
        # Récupérer la position depuis les paramètres de la requête
        position = request.args.get('position', type=int)

        # Vérifier si la position est donnée
        if position is None:
            return jsonify({"error": "Le paramètre 'position' est manquant"}), 400

        # Récupérer la question avec cette position
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, titre, texte, image, position
            FROM question
            WHERE position = ?
        """, (position,))
        question = cursor.fetchone()

        # Si aucune question n'est trouvée pour cette position
        if not question:
            return jsonify({"error": f"Aucune question trouvée pour la position {position}"}), 404

        # Ajouter les réponses possibles à la question
        cursor.execute("""
            SELECT answer_text, is_correct
            FROM answers
            WHERE question_id = ?
        """, (question["id"],))
        possible_answers = cursor.fetchall()

        # Préparer la réponse avec le format attendu
        response = {
            "id": question["id"],
            "title": question["titre"],
            "text": question["texte"],
            "position": question["position"],
            "image": question["image"],
            "possibleAnswers": [
                {"text": answer["answer_text"], "isCorrect": bool(answer["is_correct"])}
                for answer in possible_answers
            ]
        }

        conn.close()
        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 6 - Update question at position (avec authentification)
@bp.route('/questions/<int:question_id>', methods=['PUT'])
@cross_origin(origin='*')  # Permet toutes les origines
def update_question(question_id):
    try:
        authenticate()

        payload = request.get_json()
        required_fields = ['title', 'text', 'image', 'position', 'possibleAnswers']

        # Vérification des champs requis
        if not all(field in payload for field in required_fields):
            return jsonify({"error": "Champs manquants"}), 400

        # Extraire les données
        title = payload['title']
        text = payload['text']
        image = payload['image']
        new_position = payload['position']
        possible_answers = payload['possibleAnswers']

        # Appeler la fonction du service pour mettre à jour la question
        update_question_in_db(question_id, title, text, image, new_position, possible_answers)

        # Retourner une réponse vide avec le statut 204
        return '', 204

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/questions', methods=['GET'])
@cross_origin(origin='*')  # Permet toutes les origines
def get_all_questions():
    """
    Récupère toutes les questions avec leurs réponses associées.
    """
    try:
        # Appeler le service pour récupérer toutes les questions
        questions = get_all_questions_from_db()
        return jsonify(questions), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@bp.route('/questions/<int:position>', methods=['GET'])
@cross_origin(origin='*')  # Permet toutes les origines
def get_question_by_position(position):
    """
    Récupère une question spécifique par sa position.
    """
    try:
        # Appeler le service pour récupérer une question par position
        question = get_question_by_position_from_db(position)
        return jsonify(question), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500