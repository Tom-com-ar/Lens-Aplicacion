import mysql.connector
from mysql.connector import Error
import bcrypt 

class Database:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                print("Conexión a la base de datos MySQL exitosa")
        except Error as e:
            print(f"Error al conectar a MySQL: {e}")

    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Conexión a la base de datos MySQL cerrada")

    def execute_query(self, query, params=None):
        cursor = None
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            cursor = self.connection.cursor(dictionary=True) 
            cursor.execute(query, params)
            if query.strip().upper().startswith(("INSERT", "UPDATE", "DELETE")):
                self.connection.commit()
                return cursor.rowcount
            else:
                return cursor.fetchall()
        except Error as e:
            print(f"Error ejecutando la consulta: {e}")
            if self.connection:
                self.connection.rollback()
            return None
        finally:
            if cursor:
                cursor.close()

    # --- Funciones de seguridad (bcrypt) ---
    def hash_password(self, password):
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed.decode('utf-8') # Guardar como string utf-8

    def check_password(self, password, hashed_password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    # --- Funciones específicas para Comentarios ---
    def add_comentario(self, id_usuario, tmdb_id, comentario, valoracion):
        query = """
        INSERT INTO comentarios (id_usuario, tmdb_id, comentario, valoracion, fecha_comentario)
        VALUES (%s, %s, %s, %s, CURDATE())
        """
        return self.execute_query(query, (id_usuario, tmdb_id, comentario, valoracion))

    def get_comentarios_by_tmdb_id(self, tmdb_id):
        query = """
        SELECT c.*, u.nombre_usuario 
        FROM comentarios c
        JOIN usuarios u ON c.id_usuario = u.id_usuario
        WHERE c.tmdb_id = %s
        ORDER BY c.fecha_comentario DESC
        """
        return self.execute_query(query, (tmdb_id,))
    
    # --- Funciones específicas para Entradas ---
    def add_entrada(self, id_usuario, tmdb_id, fila, numero_asiento):
        query = """
        INSERT INTO entradas (id_usuario, tmdb_id, fila, numero_asiento, fecha_compra)
        VALUES (%s, %s, %s, %s, NOW())
        """
        return self.execute_query(query, (id_usuario, tmdb_id, fila, numero_asiento))

    def get_entradas_ocupadas_by_tmdb_id(self, tmdb_id):
        query = """
        SELECT fila, numero_asiento 
        FROM entradas 
        WHERE tmdb_id = %s
        """
        return self.execute_query(query, (tmdb_id,))
    
    # --- Funciones para Usuarios (para login/registro si es necesario) ---
    def get_user_by_email(self, email):
        query = "SELECT * FROM usuarios WHERE email = %s"
        users = self.execute_query(query, (email,))
        return users[0] if users else None

    def get_user_by_id(self, user_id):
        query = "SELECT id_usuario, nombre_usuario, email, fecha_registro FROM usuarios WHERE id_usuario = %s"
        user = self.execute_query(query, (user_id,))
        return user[0] if user else None

    def add_user(self, nombre_usuario, email, password):
        # Hashear la contraseña antes de guardarla
        hashed_password = self.hash_password(password)
        query = """
        INSERT INTO usuarios (nombre_usuario, email, password_hash, fecha_registro)
        VALUES (%s, %s, %s, NOW())
        """
        return self.execute_query(query, (nombre_usuario, email, hashed_password))

# Configuración de la base de datos
DB_CONFIG = {
    "host": "localhost",
    "database": "lens", 
    "user": "root",
    "password": "" 
}

# Instancia global de la base de datos
db = Database(**DB_CONFIG) 