#base/controllers/usuarios.py

from flask import render_template, redirect, request, session, Blueprint, flash
from base.models.usuarios_models import Usuario
from werkzeug.security import generate_password_hash, check_password_hash


bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')


@bp.route('/procesar_registro', methods=['POST'])
def procesar_registro():
    if not Usuario.validar_registro(request.form):
        # si la validación falla, volver al formulario de registro para ver los flashes
        return redirect('/register')
   
    # Usar generate_password_hash (devuelve str) en lugar de bcrypt para compatibilidad
    password_hash = generate_password_hash(request.form['password'])
    data = {
        **request.form,
        'password': password_hash
    }
   
    try:
        usuario_id = Usuario.guardar_usuario(data)
    except Exception as e:
        print('Error guardando usuario:', e)
        flash('Ocurrió un error al registrar el usuario. Intenta nuevamente.', 'registro')
        return redirect('/register')

    if not usuario_id:
        flash('No se pudo crear la cuenta. Contacta al administrador.', 'registro')
        return redirect('/register')

    session['usuario_id'] = usuario_id
    flash("¡Registro exitoso!", 'exito')
    return redirect('/dashboard')

@bp.route('/procesar_login', methods=['POST'])
def procesar_login():
    if not Usuario.validar_login(request.form):
        return redirect('/')
   
    # Diagnóstico: intentar obtener usuario y reportar resultados mínimos
    usuario_db = Usuario.obtener_por_email(request.form)
    if not usuario_db:
        print(f"Login fallido: usuario con email {request.form.get('email')} no encontrado")
        flash("Email o contraseña inválidos.", 'login')
        return redirect('/')

    # Verificar contraseña (Usuario.validar_login ya hace esto, mantendremos una verificación redundante para diagnóstico)
    try:
        password_ok = check_password_hash(usuario_db.password or '', request.form.get('password', ''))
    except Exception as e:
        password_ok = False
        print('Error verificando contraseña:', e)

    print(f"Login attempt for {usuario_db.email}: user_found=True, password_ok={password_ok}")

    if not password_ok:
        flash("Email o contraseña inválidos.", 'login')
        return redirect('/')

    session['usuario_id'] = usuario_db.id
    flash(f"!Bienvenido de nuevo, {usuario_db.nombre}!", 'exito')
    return redirect('/dashboard')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')