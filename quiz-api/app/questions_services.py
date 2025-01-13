from app.models import get_db_connection
from flask import jsonify
import sqlite3

def get_quiz_info_from_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Compter le nombre de questions dans la table "question"
        cursor.execute("SELECT COUNT(*) FROM question")
        question_count = cursor.fetchone()[0]

        # Récupérer les scores de la table "participations"
        cursor.execute("SELECT score FROM participations")
        scores = [row[0] for row in cursor.fetchall()]  # Liste des scores

        conn.close()

        # Retourner les données dynamiques
        return {"size": question_count, "scores": scores}

    except Exception as e:
        raise Exception(f"Erreur lors de la récupération des informations du quiz : {str(e)}")


def add_question_to_db(title, text, image, position, possible_answers):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Décaler les questions existantes si la position est déjà utilisée
        cursor.execute("""
            UPDATE question
            SET position = position + 1
            WHERE position >= ?
        """, (position,))

        # Insérer la nouvelle question
        cursor.execute("""
            INSERT INTO question (titre, texte, image, position)
            VALUES (?, ?, ?, ?)
        """, (title, text, image, position))
        question_id = cursor.lastrowid

        # Insérer les réponses
        for answer in possible_answers:
            cursor.execute("""
                INSERT INTO answers (question_id, answer_text, is_correct)
                VALUES (?, ?, ?)
            """, (question_id, answer['text'], answer['isCorrect']))

        conn.commit()
        conn.close()

        return question_id
    except Exception as e:
        raise Exception(f"Error in adding question: {str(e)}")


def delete_question_by_position_from_db(position):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Vérifier si une question existe à la position donnée
        cursor.execute("SELECT id FROM question WHERE position = ?", (position,))
        question = cursor.fetchone()

        if not question:
            raise Exception(f"Aucune question trouvée à la position {position}")

        question_id = question[0]

        # Supprimer les réponses associées
        cursor.execute("DELETE FROM answers WHERE question_id = ?", (question_id,))

        # Supprimer la question elle-même
        cursor.execute("DELETE FROM question WHERE position = ?", (position,))

        # Réajuster les positions des questions restantes
        cursor.execute("""
            UPDATE question
            SET position = position - 1
            WHERE position > ?
        """, (position,))

        # Valider les changements
        conn.commit()

    except Exception as e:
        # Roulback en cas d'erreur
        conn.rollback()
        raise Exception(f"Erreur lors de la suppression de la question à la position {position}: {str(e)}")

    finally:
        conn.close()




def delete_all_questions_from_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Supprimer toutes les réponses et toutes les questions
        cursor.execute("DELETE FROM answers")
        cursor.execute("DELETE FROM question")

        # Réinitialiser le compteur d'auto-incrémentation pour la table question
        cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'question'")

        conn.commit()
        conn.close()
    except Exception as e:
        raise Exception(f"Error in deleting all questions: {str(e)}")
    
    
def update_question_in_db(question_id, title, text, image, new_position, possible_answers):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Récupérer la position actuelle de la question
        cursor.execute("SELECT position FROM question WHERE id = ?", (question_id,))
        current_position = cursor.fetchone()
        if not current_position:
            raise Exception(f"Question avec ID {question_id} non trouvée")
        current_position = current_position[0]

        # Si la nouvelle position est différente, gérer les décalages
        if current_position != new_position:
            if new_position < current_position:
                # Déplacer vers le haut
                cursor.execute("""
                    UPDATE question
                    SET position = position + 1
                    WHERE position >= ? AND position < ?
                """, (new_position, current_position))
            else:
                # Déplacer vers le bas
                cursor.execute("""
                    UPDATE question
                    SET position = position - 1
                    WHERE position > ? AND position <= ?
                """, (current_position, new_position))

        # Mettre à jour les champs de la question
        cursor.execute("""
            UPDATE question
            SET titre = ?, texte = ?, image = ?, position = ?
            WHERE id = ?
        """, (title, text, image, new_position, question_id))

        # Supprimer les anciennes réponses
        cursor.execute("DELETE FROM answers WHERE question_id = ?", (question_id,))

        # Ajouter les nouvelles réponses
        for answer in possible_answers:
            cursor.execute("""
                INSERT INTO answers (question_id, answer_text, is_correct)
                VALUES (?, ?, ?)
            """, (question_id, answer['text'], answer['isCorrect']))

        conn.commit()
        conn.close()

    except sqlite3.IntegrityError as e:
        raise Exception(f"Erreur d'intégrité dans la mise à jour de la question : {str(e)}")
    except Exception as e:
        raise Exception(f"Erreur dans la mise à jour de la question : {str(e)}")

def get_all_questions_from_db():
    """
    Récupère toutes les questions avec leurs réponses associées.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Récupérer toutes les questions
        cursor.execute("SELECT * FROM question")
        questions = cursor.fetchall()

        result = []
        for question in questions:
            cursor.execute("""
                SELECT id, answer_text, is_correct
                FROM answers
                WHERE question_id = ?
            """, (question['id'],))
            answers = cursor.fetchall()

            result.append({
                "id": question['id'],
                "title": question['titre'],
                "text": question['texte'],
                "image": question['image'],
                "position": question['position'],
                "possibleAnswers": [
                    {"id": answer['id'], "text": answer['answer_text'], "isCorrect": answer['is_correct']}
                    for answer in answers
                ]
            })

        conn.close()
        return result

    except Exception as e:
        raise Exception(f"Error in fetching all questions: {str(e)}")


def get_question_by_position_from_db(position):
    """
    Récupère une question par position avec ses réponses associées.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Récupérer la question par position
        cursor.execute("SELECT * FROM question WHERE position = ?", (position,))
        question = cursor.fetchone()

        if not question:
            raise Exception(f"Question avec la position {position} non trouvée")

        # Récupérer les réponses associées à la question
        cursor.execute("""
            SELECT id, answer_text, is_correct
            FROM answers
            WHERE question_id = ?
        """, (question['id'],))  # Utilisation correcte de question['id']
        answers = cursor.fetchall()

        conn.close()
        # Construire la réponse
        return {
            "id": question["id"],
            "title": question["titre"],
            "text": question["texte"],
            "image": question["image"],
            "position": question["position"],
            "possibleAnswers": [
                {"id": answer["id"], "text": answer["answer_text"], "isCorrect": answer["is_correct"]}
                for answer in answers
            ]
        }

    except Exception as e:
        raise Exception(f"Error in fetching question by position: {str(e)}")




def delete_question_by_position_from_db(position):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Vérifier si une question existe à la position donnée
        cursor.execute("SELECT id FROM question WHERE position = ?", (position,))
        question = cursor.fetchone()

        if not question:
            raise Exception(f"Aucune question trouvée à la position {position}")

        question_id = question[0]

        # Supprimer les réponses associées
        cursor.execute("DELETE FROM answers WHERE question_id = ?", (question_id,))

        # Supprimer la question elle-même
        cursor.execute("DELETE FROM question WHERE position = ?", (position,))

        # Réajuster les positions des questions restantes
        cursor.execute("""
            UPDATE question
            SET position = position - 1
            WHERE position > ?
        """, (position,))

        # Valider les changements
        conn.commit()

    except Exception as e:
        # Roulback en cas d'erreur
        conn.rollback()
        raise Exception(f"Erreur lors de la suppression de la question à la position {position}: {str(e)}")

    finally:
        conn.close()
