from django.db import connection
from datetime import datetime


class UserModel:
    @staticmethod
    def create_user(
        first_name, last_name, email, password, phone, dob, gender, address, role_type
    ):
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO users (first_name, last_name, email, password, phone, dob, gender, address, role_type, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                RETURNING id;
            """
            cursor.execute(
                sql,
                (
                    first_name,
                    last_name,
                    email,
                    password,
                    phone,
                    dob,
                    gender,
                    address,
                    role_type,
                ),
            )
            return cursor.fetchone()[0]

    @staticmethod
    def get_user_by_email(email):
        """
        Retrieves a user by their email using raw SQL.
        """
        with connection.cursor() as cursor:
            sql = "SELECT * FROM users WHERE email = %s;"
            cursor.execute(sql, [email])
            row = cursor.fetchone()
            if row:
                columns = [col[0] for col in cursor.description]
                return dict(zip(columns, row))
            return None

    @staticmethod
    def get_user_by_id(user_id):
        """
        Retrieves a user by their ID using raw SQL.
        """
        with connection.cursor() as cursor:
            sql = "SELECT * FROM users WHERE id = %s;"
            cursor.execute(sql, [user_id])
            row = cursor.fetchone()
            if row:
                columns = [col[0] for col in cursor.description]
                return dict(zip(columns, row))
            return None