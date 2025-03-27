from django.db import connection


class MusicModel:
    @staticmethod
    def create_music(title, artist_id, album_name, genre):
        """Insert a new music record into the database."""
        genre = (
            genre.lower()
        )  # Convert genre to lowercase for PostgreSQL enum compatibility

        with connection.cursor() as cursor:
            sql = """
                INSERT INTO music (title, artist_id, album_name, genre, created_at, updated_at)
                VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                RETURNING id;
            """
            cursor.execute(sql, (title, artist_id, album_name, genre))
            return cursor.fetchone()[0]

    @staticmethod
    def get_all_music():
        """Fetch all music records along with the artist name."""
        with connection.cursor() as cursor:
            sql = """
                SELECT 
                    m.id, 
                    m.title, 
                    a.name AS artist_name,  -- Fetch artist name instead of ID
                    m.album_name, 
                    m.genre, 
                    m.created_at, 
                    m.updated_at
                FROM music m
                LEFT JOIN artist a ON m.artist_id = a.id;  -- Join to fetch artist name
            """
            cursor.execute(sql)
            return cursor.fetchall()  # Returns a list of tuples

    @staticmethod
    def get_music_by_id(music_id):
        """Fetch a single music record by ID along with the artist name."""
        with connection.cursor() as cursor:
            sql = """
                SELECT 
                    m.id, 
                    m.title, 
                    a.name AS artist_name,  -- Fetch artist name instead of ID
                    m.album_name, 
                    m.genre, 
                    m.created_at, 
                    m.updated_at
                FROM music m
                LEFT JOIN artist a ON m.artist_id = a.id
                WHERE m.id = %s;
            """
            cursor.execute(sql, [music_id])
            return cursor.fetchone()  # Returns a single tuple or None

    @staticmethod
    def update_music(music_id, title, artist_id, album_name, genre):
        """Update a music record."""
        genre = genre.lower()  # Convert genre to lowercase before updating

        with connection.cursor() as cursor:
            sql = """
                UPDATE music
                SET title = %s, artist_id = %s, album_name = %s, genre = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s;
            """
            cursor.execute(sql, (title, artist_id, album_name, genre, music_id))
            return cursor.rowcount > 0  # Returns True if at least one row was updated

    @staticmethod
    def delete_music(music_id):
        """Delete a music record."""
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM music WHERE id = %s;", [music_id])
            return cursor.rowcount > 0  # Returns True if at least one row was deleted
