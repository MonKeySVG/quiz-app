from flask import Blueprint, request, jsonify
from app.participations_services import calculate_score_and_save, get_all_participations, delete_all_participations, delete_participation_by_id
from flask_cors import cross_origin

bp = Blueprint('participations', __name__)

@bp.route('/participations', methods=['POST'])
@cross_origin(origin='*')  # Permet toutes les origines
def add_participation():
    """
    Enregistre une participation et calcule le score.
    """
    try:
        data = request.get_json()

        player_name = data.get("playerName")
        answers = data.get("answers")

        # Valider les données
        if not player_name or not answers or not isinstance(answers, list):
            return jsonify({"error": "playerName et answers sont requis"}), 400
        
        # Vérification du nombre de réponses
        if len(answers) != 10:
            return jsonify({"error": "La liste des réponses doit contenir exactement 10 éléments"}), 400

        # Calculer le score et enregistrer la participation
        result = calculate_score_and_save(player_name, answers)

        # Répondre avec le score calculé
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@bp.route('/participations', methods=['GET'])
@cross_origin(origin='*')  # Permet toutes les origines
def get_participations():
    """
    Récupère toutes les participations.
    """
    try:
        participations = get_all_participations()
        return jsonify(participations), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@bp.route('/participations/all', methods=['DELETE'])
@cross_origin(origin='*')  # Permet toutes les origines
def clear_participations():
    """
    Supprime toutes les participations.
    """
    try:
        delete_all_participations()
        return jsonify({"message": "Toutes les participations ont été supprimées"}), 204

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@bp.route('/participations/<int:id>', methods=['DELETE'])
@cross_origin(origin='*')  # Permet toutes les origines
def remove_participation(id):
    """
    Supprime une participation spécifique par son ID.
    """
    try:
        if delete_participation_by_id(id):
            return jsonify({"message": f"Participation avec ID {id} supprimée"}), 200
        else:
            return jsonify({"error": "Participation non trouvée"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
