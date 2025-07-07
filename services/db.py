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
            # Solo reconectar si no hay conexión activa
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
    def add_comentario(self, id_usuario, id_pelicula, comentario, valoracion):
        query = """
        INSERT INTO comentarios (id_usuario, id_pelicula, comentario, valoracion, fecha_comentario)
        VALUES (%s, %s, %s, %s, CURDATE())
        """
        return self.execute_query(query, (id_usuario, id_pelicula, comentario, valoracion))

    def get_comentarios_by_pelicula(self, id_pelicula):
        query = """
        SELECT c.*, u.nombre_usuario 
        FROM comentarios c
        JOIN usuarios u ON c.id_usuario = u.id_usuario
        WHERE c.id_pelicula = %s
        ORDER BY c.fecha_comentario DESC
        """
        return self.execute_query(query, (id_pelicula,))
    
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
        query = "SELECT id_usuario, nombre_usuario, email, fecha_registro, rol FROM usuarios WHERE id_usuario = %s"
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

    # --- Funciones para Películas ---
    def get_peliculas(self):
        query = "SELECT * FROM peliculas WHERE estado = 'activa' ORDER BY fecha_agregada DESC"
        return self.execute_query(query)

    def get_pelicula_by_id(self, id_pelicula):
        query = "SELECT * FROM peliculas WHERE id_pelicula = %s"
        result = self.execute_query(query, (id_pelicula,))
        return result[0] if result else None

    # --- Funciones para Funciones (proyecciones) ---
    def get_funciones_by_pelicula(self, id_pelicula):
        query = """
        SELECT f.*, s.nombre as nombre_sala, s.capacidad
        FROM funciones f
        JOIN salas s ON f.id_sala = s.id_sala
        WHERE f.id_pelicula = %s AND f.fecha_hora >= NOW()
        ORDER BY f.fecha_hora ASC
        """
        return self.execute_query(query, (id_pelicula,))

    def get_funcion_by_id(self, id_funcion):
        query = "SELECT * FROM funciones WHERE id_funcion = %s"
        result = self.execute_query(query, (id_funcion,))
        return result[0] if result else None

    # --- Funciones para Salas ---
    def get_sala_by_id(self, id_sala):
        query = "SELECT * FROM salas WHERE id_sala = %s"
        result = self.execute_query(query, (id_sala,))
        return result[0] if result else None

    # --- Entradas asociadas a función ---
    def add_entrada_funcion(self, id_usuario, id_funcion, fila, numero_asiento):
        # Debes obtener el id_pelicula correspondiente a la función
        funcion = self.get_funcion_by_id(id_funcion)
        if not funcion:
            return None
        id_pelicula = funcion["id_pelicula"]
        query = """
        INSERT INTO entradas (id_usuario, id_pelicula, id_funcion, fila, numero_asiento, fecha_compra)
        VALUES (%s, %s, %s, %s, %s, NOW())
        """
        return self.execute_query(query, (id_usuario, id_pelicula, id_funcion, fila, numero_asiento))

    def get_entradas_ocupadas_by_funcion(self, id_funcion):
        query = "SELECT fila, numero_asiento FROM entradas WHERE id_funcion = %s"
        return self.execute_query(query, (id_funcion,))

    def get_entradas_by_usuario(self, id_usuario):
        query = """
        SELECT e.*, p.titulo as titulo_pelicula, f.fecha_hora, s.nombre as nombre_sala
        FROM entradas e
        JOIN peliculas p ON e.id_pelicula = p.id_pelicula
        JOIN funciones f ON e.id_funcion = f.id_funcion
        JOIN salas s ON f.id_sala = s.id_sala
        WHERE e.id_usuario = %s
        ORDER BY e.fecha_compra DESC
        """
        return self.execute_query(query, (id_usuario,))

    def get_comentarios_by_usuario(self, id_usuario):
        query = """
        SELECT c.*, p.titulo as titulo_pelicula
        FROM comentarios c
        JOIN peliculas p ON c.id_pelicula = p.id_pelicula
        WHERE c.id_usuario = %s
        ORDER BY c.fecha_comentario DESC
        """
        return self.execute_query(query, (id_usuario,))

    # --- Estadísticas para panel admin ---
    def count_peliculas_total(self):
        query = "SELECT COUNT(*) as total FROM peliculas"
        result = self.execute_query(query)
        return result[0]["total"] if result else 0

    def count_peliculas_api(self):
        query = "SELECT COUNT(*) as total FROM peliculas WHERE origen = 'api'"
        result = self.execute_query(query)
        return result[0]["total"] if result else 0

    def count_peliculas_manuales(self):
        query = "SELECT COUNT(*) as total FROM peliculas WHERE origen = 'manual'"
        result = self.execute_query(query)
        return result[0]["total"] if result else 0

    def count_usuarios(self):
        query = "SELECT COUNT(*) as total FROM usuarios"
        result = self.execute_query(query)
        return result[0]["total"] if result else 0

    def count_comentarios(self):
        query = "SELECT COUNT(*) as total FROM comentarios"
        result = self.execute_query(query)
        return result[0]["total"] if result else 0

    def count_entradas(self):
        query = "SELECT COUNT(*) as total FROM entradas"
        result = self.execute_query(query)
        return result[0]["total"] if result else 0

    # --- Funciones adicionales para eliminaciones seguras ---
    def delete_pelicula_safe(self, id_pelicula):
        """Elimina una película de forma segura, verificando dependencias"""
        try:
            # Verificar si hay funciones asociadas
            funciones = self.execute_query("SELECT COUNT(*) as total FROM funciones WHERE id_pelicula = %s", (id_pelicula,))
            if funciones and funciones[0]["total"] > 0:
                return False, "No se puede eliminar la película porque tiene funciones asociadas"
            
            # Verificar si hay comentarios asociados
            comentarios = self.execute_query("SELECT COUNT(*) as total FROM comentarios WHERE id_pelicula = %s", (id_pelicula,))
            if comentarios and comentarios[0]["total"] > 0:
                return False, "No se puede eliminar la película porque tiene comentarios asociados"
            
            # Verificar si hay entradas asociadas
            entradas = self.execute_query("SELECT COUNT(*) as total FROM entradas WHERE id_pelicula = %s", (id_pelicula,))
            if entradas and entradas[0]["total"] > 0:
                return False, "No se puede eliminar la película porque tiene entradas asociadas"
            
            # Si no hay dependencias, eliminar la película
            result = self.execute_query("DELETE FROM peliculas WHERE id_pelicula = %s", (id_pelicula,))
            return True, "Película eliminada correctamente"
        except Exception as e:
            return False, f"Error al eliminar: {str(e)}"

    def delete_sala_safe(self, id_sala):
        """Elimina una sala de forma segura, verificando dependencias"""
        try:
            # Verificar si hay funciones asociadas
            funciones = self.execute_query("SELECT COUNT(*) as total FROM funciones WHERE id_sala = %s", (id_sala,))
            if funciones and funciones[0]["total"] > 0:
                return False, "No se puede eliminar la sala porque tiene funciones asociadas"
            
            # Si no hay dependencias, eliminar la sala
            result = self.execute_query("DELETE FROM salas WHERE id_sala = %s", (id_sala,))
            return True, "Sala eliminada correctamente"
        except Exception as e:
            return False, f"Error al eliminar: {str(e)}"

    def delete_funcion_safe(self, id_funcion):
        """Elimina una función de forma segura, verificando dependencias"""
        try:
            # Verificar si hay entradas asociadas
            entradas = self.execute_query("SELECT COUNT(*) as total FROM entradas WHERE id_funcion = %s", (id_funcion,))
            if entradas and entradas[0]["total"] > 0:
                return False, "No se puede eliminar la función porque tiene entradas vendidas"
            
            # Si no hay dependencias, eliminar la función
            result = self.execute_query("DELETE FROM funciones WHERE id_funcion = %s", (id_funcion,))
            return True, "Función eliminada correctamente"
        except Exception as e:
            return False, f"Error al eliminar: {str(e)}"

    def get_peliculas_with_stats(self):
        """Obtiene películas con estadísticas adicionales"""
        query = """
        SELECT p.*, 
               COALESCE(f_stats.total_funciones, 0) as total_funciones,
               COALESCE(c_stats.total_comentarios, 0) as total_comentarios,
               COALESCE(e_stats.total_entradas, 0) as total_entradas
        FROM peliculas p
        LEFT JOIN (
            SELECT id_pelicula, COUNT(*) as total_funciones 
            FROM funciones 
            GROUP BY id_pelicula
        ) f_stats ON p.id_pelicula = f_stats.id_pelicula
        LEFT JOIN (
            SELECT id_pelicula, COUNT(*) as total_comentarios 
            FROM comentarios 
            GROUP BY id_pelicula
        ) c_stats ON p.id_pelicula = c_stats.id_pelicula
        LEFT JOIN (
            SELECT id_pelicula, COUNT(*) as total_entradas 
            FROM entradas 
            GROUP BY id_pelicula
        ) e_stats ON p.id_pelicula = e_stats.id_pelicula
        WHERE p.estado = 'activa'
        ORDER BY p.fecha_agregada DESC
        """
        return self.execute_query(query)

    def get_salas_with_stats(self):
        """Obtiene salas con estadísticas adicionales"""
        query = """
        SELECT s.*, 
               COALESCE(f_stats.total_funciones, 0) as total_funciones
        FROM salas s
        LEFT JOIN (
            SELECT id_sala, COUNT(*) as total_funciones 
            FROM funciones 
            GROUP BY id_sala
        ) f_stats ON s.id_sala = f_stats.id_sala
        ORDER BY s.id_sala ASC
        """
        return self.execute_query(query)

    def get_funciones_with_stats(self):
        """Obtiene funciones con estadísticas adicionales"""
        query = """
        SELECT f.*, p.titulo, s.nombre as nombre_sala, p.duracion,
               COALESCE(e_stats.entradas_vendidas, 0) as entradas_vendidas
        FROM funciones f
        JOIN peliculas p ON f.id_pelicula = p.id_pelicula
        JOIN salas s ON f.id_sala = s.id_sala
        LEFT JOIN (
            SELECT id_funcion, COUNT(*) as entradas_vendidas 
            FROM entradas 
            GROUP BY id_funcion
        ) e_stats ON f.id_funcion = e_stats.id_funcion
        ORDER BY f.fecha_hora DESC
        """
        return self.execute_query(query)

# Configuración de la base de datos
DB_CONFIG = {
    "host": "localhost",
    "database": "lens", 
    "user": "root",
    "password": "" 
}

# Instancia global de la base de datos
db = Database(**DB_CONFIG)