# Archivo: user_repository.py

from infraestructure.connection import Connection
from models.user import User
import bcrypt

class UserRepository:
    def __init__(self, conn: Connection) -> None:
        self.__conn = conn

    def create_user(self, user: User) -> User:
        try:
            # Verifica si el usuario ya existe en la base de datos
            sql_check = "SELECT COUNT(*) FROM users WHERE name = %s"
            self.__conn.execute(sql_check, (user.get_name(),))
            result = self.__conn.fetchone()

            if result[0] > 0:
                raise ValueError(f"El nombre de usuario '{user.get_name()}' ya está registrado.")

            # Inserta el nuevo usuario
            sql_insert = "INSERT INTO users (name, password) VALUES (%s, %s)"
            self.__conn.execute(sql_insert, (
                user.get_name(),
                user.get_password()
            ))
            self.__conn.commit()

            return user

        except Exception as e:
            print(f"Error al crear usuario: {e}")
            raise e

    def login_user(self, name: str, password: str) -> User:
        try:
            sql = "SELECT id, name, password FROM users WHERE name = %s"
            self.__conn.execute(sql, (name,))
            
            result = self.__conn.fetchone()
            
            if not result:
                return None

            stored_password = str(result[2])

            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                user = User()
                user.set_id(result[0])
                user.set_name(result[1])
                return user
            else:
                return None

        except Exception as e:
            print(f"Error al iniciar sesión: {e}")
            return None
