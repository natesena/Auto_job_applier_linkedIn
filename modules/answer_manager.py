import sqlite3
from difflib import get_close_matches
import os

class AnswerManager:
    DB_FILE = 'config/learned_answers.db'

    def __init__(self):
        self.init_db()

    def init_db(self):
        os.makedirs(os.path.dirname(self.DB_FILE), exist_ok=True)
        with sqlite3.connect(self.DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS learned_answers (
                id INTEGER PRIMARY KEY,
                question TEXT UNIQUE,
                answer TEXT,
                last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            conn.commit()

    def get_learned_answer(self, question, threshold=0.8):
        with sqlite3.connect(self.DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT question, answer FROM learned_answers')
            all_qa = cursor.fetchall()
            questions = [qa[0] for qa in all_qa]
            close_matches = get_close_matches(question, questions, n=1, cutoff=threshold)
            if close_matches:
                cursor.execute('SELECT answer FROM learned_answers WHERE question = ?', (close_matches[0],))
                return cursor.fetchone()[0]
        return None

    def update_learned_answer(self, question, answer):
        with sqlite3.connect(self.DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT OR REPLACE INTO learned_answers (question, answer, last_used)
            VALUES (?, ?, CURRENT_TIMESTAMP)
            ''', (question, answer))
            conn.commit()

    def review_learned_answers(self):
        with sqlite3.connect(self.DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT question, answer FROM learned_answers ORDER BY last_used DESC')
            for question, answer in cursor.fetchall():
                print(f"Question: {question}")
                print(f"Current Answer: {answer}")
                new_answer = input("Enter new answer (or press Enter to keep current): ")
                if new_answer:
                    cursor.execute('UPDATE learned_answers SET answer = ?, last_used = CURRENT_TIMESTAMP WHERE question = ?', (new_answer, question))
            conn.commit()

    def get_all_answers(self):
        with sqlite3.connect(self.DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT question, answer FROM learned_answers ORDER BY last_used DESC')
            return cursor.fetchall()

answer_manager = AnswerManager()
