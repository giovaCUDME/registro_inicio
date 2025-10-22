# base/models/usuarios_models.py
# Modelo de Usuario

from base.config.pymysqlconnection import connectToMySQL
import re
from flask import flash
from werkzeug.security import check_password_hash
import os

# Expresión regular para validar emails
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9]+\.[a-zA-Z]+$')

class Usuario:
    """
    Clase que representa a un usuario y sus operaciones en la base de datos.
    """
    # Nombre de la base de datos. Puede configurarse mediante la variable de entorno
    # `APP_DB_NAME`. Si no está presente, usa 'registro' como valor por defecto.
    db = os.environ.get('APP_DB_NAME', 'registro')

    def __init__(self, data):
        """
        Constructor: inicializa los atributos del usuario
        """
        data = data or {}
        self.id = data.get('id')
        self.nombre = (data.get('nombre') or '').strip().capitalize()
        self.apellido = (data.get('apellido') or '').strip().capitalize()
        self.email = data.get('email')
        self.password = data.get('password')
        self.create_at = data.get('create_at')
        self.updated_at = data.get('updated_at')

    @classmethod
    def guardar_usuario(cls, data):
        """
        Guardar un nuevo usuario en la base de datos
        """
        if 'nombre' in data and data['nombre']:
            data['nombre'] = data['nombre'].strip().capitalize()
        if 'apellido' in data and data['apellido']:
            data['apellido'] = data['apellido'].strip().capitalize()
        query = (
            "INSERT INTO usuarios (nombre, apellido, email, password) "
            "VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s);"
        )
        try:
            insert_id = connectToMySQL(cls.db).query_db(query, data)
            return insert_id
        except Exception as e:
            # Debug: imprimir error y parámetros para diagnóstico
            print('Error en guardar_usuario:', e)
            print('Query:', query)
            print('Data:', data)
            return None

    @classmethod
    def obtener_por_email(cls, data):
        """
        Buscar un usuario por su email.
        """
        email = None
        if isinstance(data, dict):
            email = data.get('email')
        else:
            email = data
        if not email:
            return None
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        resultado = connectToMySQL(cls.db).query_db(query, {'email': email})
        if not resultado:
            return None
        return cls(resultado[0])
   
    @classmethod
    def obtener_por_id(cls, usuario_id):
        """
        Buscar un usuario por su ID
        """
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        data = {'id': usuario_id}
        resultado = connectToMySQL(cls.db).query_db(query, data)
        if not resultado:
            return None
        return cls(resultado[0])
   
    @staticmethod
    def validar_registro(usuario):
        """
        Valida los datos del formulario de registro.
        Devuelve True si todo es válido, False si hay errores (y los muestra con flash).
        """
        is_valid = True
        # Comprueba si el email ya existe
        query = "SELECT id FROM usuarios WHERE email = %(email)s;"
        resultado = connectToMySQL(Usuario.db).query_db(query, {'email': usuario.get('email')})
        if resultado:
            flash("El email ya está registrado.", 'registro')
            is_valid = False

        # Validaciones de formato
        email_val = usuario.get('email', '')
        if not EMAIL_REGEX.match(email_val):
            flash("Formato de email inválido.", 'registro')
            is_valid = False

        nombre = usuario.get('nombre', '')
        apellido = usuario.get('apellido', '')
        if len(nombre) < 3:
            flash("El nombre debe tener al menos 3 caracteres.", 'registro')
            is_valid = False
        if len(apellido) < 3:
            flash("El apellido debe tener al menos 3 caracteres.", 'registro')
            is_valid = False

        password = usuario.get('password', '')
        confirm = usuario.get('confirm_password', '')
        if len(password) < 8:
            flash("La contraseña debe tener al menos 8 caracteres.", 'registro')
            is_valid = False
        if password != confirm:
            flash("Las contraseñas no coinciden.", 'registro')
            is_valid = False
        return is_valid

    @staticmethod
    def validar_login(usuario):
        """
        Valida los datos del formulario de inicio de sesión.
        Devuelve True si el usuario existe y la contraseña es correcta.
        """
        # Validaciones básicas de entrada
        email = (usuario.get('email') or '').strip()
        password = usuario.get('password') or ''

        if not email:
            flash('El email es requerido.', 'login')
            return False
        if not EMAIL_REGEX.match(email):
            flash('Formato de email inválido.', 'login')
            return False
        if not password:
            flash('La contraseña es requerida.', 'login')
            return False

        # Buscar usuario en la base de datos
        user_in_db = Usuario.obtener_por_email({'email': email})
        if not user_in_db:
            flash("Email o contraseña inválidos.", 'login')
            return False

        # Comprueba la contraseña: stored password debe ser el hash
        stored_hash = user_in_db.password or ''
        try:
            # check_password_hash acepta (hash, password)
            password_ok = check_password_hash(stored_hash, password)
        except Exception:
            password_ok = False

        if not password_ok:
            flash("Email o contraseña inválidos.", 'login')
            return False

        return True