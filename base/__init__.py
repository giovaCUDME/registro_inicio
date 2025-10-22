# base/__init__.py

from flask import Flask, render_template, session, redirect
from flask import flash


def create_app():
    # indicar explícitamente la carpeta de plantillas y estáticos del paquete `base`
    app = Flask(__name__, template_folder='template', static_folder='static')
    app.secret_key = 'tu_clave_secreta_super_segura_aqui_cambiala'
    
    # Registrar el blueprint de usuarios
    from base.controllers.usuarios import bp as usuarios_bp
    app.register_blueprint(usuarios_bp)
    
    # Ruta principal - Login
    @app.route('/')
    def index():
        if 'usuario_id' in session:
            return redirect('/dashboard')
        return render_template('login.html')
    
    # Ruta de registro
    @app.route('/register')
    def register():
        if 'usuario_id' in session:
            return redirect('/dashboard')
        return render_template('register.html')
    
    # Ruta del dashboard
    @app.route('/dashboard')
    def dashboard():
        if 'usuario_id' not in session:
            flash('Debes iniciar sesión primero.', 'login')
            return redirect('/')
        
        from base.models.usuarios_models import Usuario
        usuario = Usuario.obtener_por_id(session['usuario_id'])
        if not usuario:
            session.clear()
            return redirect('/')
        
        return render_template('dashboard.html', nombre=usuario.nombre)
    
    return app