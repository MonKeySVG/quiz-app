import sqlite3
from app.models import get_db_connection

def calculate_score_and_save(player_name, score):
    """
    Calcule le score et enregistre la participation.
    :param player_name: Nom du joueur.
    :param answer_ids: Liste des IDs de réponses sélectionnées.
    :return: Un dictionnaire contenant le score calculé et le nom du joueur.
    """

    with get_db_connection() as conn:
        cursor = conn.cursor()

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

