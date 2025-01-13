import sqlite3
from app.models import get_db_connection

def calculate_score_and_save(player_name, answer_ids):
    """
    Calcule le score et enregistre la participation.
    :param player_name: Nom du joueur.
    :param answer_ids: Liste des IDs de réponses sélectionnées.
    :return: Un dictionnaire contenant le score calculé et le nom du joueur.
    """

    # Calculer le score
    score = 0
    with get_db_connection() as conn:
        cursor = conn.cursor()

        for answer_id in answer_ids:
            cursor.execute("""
                SELECT is_correct
                FROM answers
                WHERE id = ?
            """, (answer_id,))
            result = cursor.fetchone()

            if result and result["is_correct"]:  # Si la réponse est correcte
                score += 1

        # Enregistrer la participation
        cursor.execute("""
            INSERT INTO participations (player_name, score)
            VALUES (?, ?)
        """, (player_name, score))
        conn.commit()

    return {"playerName": player_name, "score": score}



def get_all_participations():
    """
    Récupère toutes les participations de la base de données.
    :return: Liste de participations.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, player_name, score
            FROM participations
        """)
        participations = cursor.fetchall()

        # Transformer les résultats en liste de dictionnaires
        return [
            {"id": row["id"], "playerName": row["player_name"], "score": row["score"]}
            for row in participations
        ]
    

def delete_all_participations():
    """
    Supprime toutes les participations de la base de données.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM participations")
        conn.commit()


def delete_participation_by_id(participation_id):
    """
    Supprime une participation spécifique par son ID.
    :param participation_id: ID de la participation à supprimer.
    :return: True si la suppression a réussi, False sinon.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM participations WHERE id = ?", (participation_id,))
        conn.commit()
        return cursor.rowcount > 0

