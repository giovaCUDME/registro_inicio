# Inicio y registro - proyecto Flask

Instrucciones rápidas para ejecutar el proyecto en Windows (PowerShell):

1) Activar el entorno virtual (desde la raíz del proyecto):

```powershell
.\mi_entorno\Scripts\Activate.ps1
```

2) Instalar dependencias (si faltan):

```powershell
python -m pip install -r requirements.txt
```

3) Ejecutar la aplicación:

```powershell
# desde la raíz del proyecto
python .\server.py
```

4) Abrir en el navegador: http://127.0.0.1:5021/

Notas:
- La aplicación usa una factory `create_app` en `base/__init__.py`.
- Configura la conexión MySQL en `base/config/pymysqlconnection.py` y pasa el nombre de la base de datos al llamar `connectToMySQL`.
- Si usas otra configuración de base de datos, actualiza las credenciales dentro de `base/config/pymysqlconnection.py` o proporciona una alternativa segura (variables de entorno).
