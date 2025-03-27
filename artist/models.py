from django.db import connection
from datetime import datetime


class ArtistModel:
    @staticmethod
    def create_artist(
        name, dob, gender, address, first_release_year, no_of_albums_released
    ):
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO artist (name, dob, gender, address, first_release_year, no_of_albums_released, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                RETURNING id;
            """
            cursor.execute(
                sql,
                (name, dob, gender, address, first_release_year, no_of_albums_released),
            )
            return cursor.fetchone()[0]

    @staticmethod
    def get_artist_by_id(artist_id):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM artist WHERE id = %s;", [artist_id])
            return cursor.fetchone()

    @staticmethod
    def get_all_artists():
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM artist;")
            return cursor.fetchall()

    @staticmethod
    def update_artist(
        artist_id, name, dob, gender, address, first_release_year, no_of_albums_released
    ):
        with connection.cursor() as cursor:
            sql = """
                UPDATE artist
                SET name = %s, dob = %s, gender = %s, address = %s, 
                    first_release_year = %s, no_of_albums_released = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s;
            """
            cursor.execute(
                sql,
                (
                    name,
                    dob,
                    gender,
                    address,
                    first_release_year,
                    no_of_albums_released,
                    artist_id,
                ),
            )
            return cursor.rowcount > 0  # Ensure it returns True if updated

    @staticmethod
    def delete_artist(artist_id):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM artist WHERE id = %s;", [artist_id])
            return cursor.rowcount > 0  # Ensure it returns True if deleted
