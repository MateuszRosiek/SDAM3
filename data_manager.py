from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import database_common
from datetime import datetime

@database_common.connection_handler
def get_column_names(cursor: RealDictCursor) -> list:
    query = """
        SELECT column_name
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = 'question';"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_questions(cursor: RealDictCursor) -> list:
    query = """
        SELECT *
        FROM question
        ORDER BY submission_time"""
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def get_sorted_questions(cursor: RealDictCursor, order_by: str, order_direction: str):
    query = f"""
            SELECT id, submission_time, view_number, vote_number, title
            FROM question
            ORDER BY {order_by} {order_direction}"""
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def vote_question_up(cursor: RealDictCursor, question_id: int):
    query = f"""
                UPDATE question
                SET vote_number = vote_number + 1
                WHERE id = '{question_id}'"""
    cursor.execute(query)

@database_common.connection_handler
def vote_question_down(cursor: RealDictCursor, question_id: int):
    query = f"""
                UPDATE question
                SET vote_number = vote_number - 1
                WHERE id = '{question_id}'"""
    cursor.execute(query)

@database_common.connection_handler
def add_question(cursor: RealDictCursor, title: str, message: str, image: str, view_number=0, vote_number=0, ) -> list:
    query = f"""
            INSERT INTO question(submission_time, view_number, vote_number, title, message, image)
            VALUES (now()::timestamptz(0), '{view_number}', '{vote_number}', '{title}','{message}', '{image}')"""
    cursor.execute(query)


@database_common.connection_handler
def add_answer(cursor: RealDictCursor, question_id: int, message: str, image: str, vote_number=0, ) -> list:
    query = f"""
            INSERT INTO answer(submission_time, vote_number, question_id, message, image)
            VALUES (now()::timestamptz(0),'{vote_number}','{question_id}','{message}', '{image}')"""
    cursor.execute(query)


@database_common.connection_handler
def delete_question(cursor: RealDictCursor, question_id: int) -> list:
    query = f"""
            DELETE FROM question
            WHERE id = '{question_id}'
            """
    cursor.execute(query)


@database_common.connection_handler
def get_latest_question_id(cursor: RealDictCursor) -> list:
    query = f"""
            SELECT id FROM question
            ORDER BY id desc
            LIMIT 1
            """
    cursor.execute(query)
    dict = cursor.fetchone()
    for key, val in dict.items():
        return val


@database_common.connection_handler
def delete_answer(cursor: RealDictCursor, answer_id: int) -> list:
    query = f"""
            DELETE FROM answer
            WHERE id = '{answer_id}'
            """
    cursor.execute(query)


@database_common.connection_handler
def get_question(cursor: RealDictCursor, question_id: int) -> list:
    query = f"""
            SELECT * FROM question
            WHERE id = '{question_id}'
            """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_answers(cursor: RealDictCursor, question_id: int) -> list:
    query = f"""
            SELECT * FROM answer
            WHERE question_id = '{question_id}'
            """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def vote_answer_up(cursor: RealDictCursor, answer_id: int):
    query = f"""
                UPDATE answer
                SET vote_number = vote_number + 1
                WHERE id = '{answer_id}'"""
    cursor.execute(query)

@database_common.connection_handler
def vote_answer_down(cursor: RealDictCursor, answer_id: int):
    query = f"""
                UPDATE answer
                SET vote_number = vote_number - 1
                WHERE id = '{answer_id}'"""
    cursor.execute(query)


@database_common.connection_handler
def get_answer_img_by_id(cursor: RealDictCursor, question_id: int, answer_id: int) -> list:
    query = f"""
        SELECT id, submission_time, vote_number, question_id, message, image 
        FROM answer
        WHERE question_id = {question_id} AND id = {answer_id}"""
    cursor.execute(query)
    return cursor.fetchall()