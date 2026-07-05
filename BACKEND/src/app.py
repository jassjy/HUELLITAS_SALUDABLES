from flask import Flask, request, jsonify, session
from flask_cors import CORS
from BACKEND.src.config import config
import os

def create_app(config_name='default'):
    """Fábrica de la aplicación API REST"""
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Habilitar CORS para el frontend
    CORS(app, origins=[
        'http://127.0.0.1:5500', 
        'http://localhost:5500',
        'http://127.0.0.1:5501',
        'http://localhost:5501',
        'http://127.0.0.1:3000',
        'http://localhost:3000'
    ], supports_credentials=True)
    
    register_api_routes(app)
    
    return app

def register_api_routes(app):
    """Registrar todas las rutas de la API REST"""
    
    # ==================== USUARIOS ====================
    
    @app.route('/api/login', methods=['POST', 'OPTIONS'])
    def api_login():
        """Inicio de sesión - API"""
        if request.method == 'OPTIONS':
            return '', 200
            
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if email and password:
            session['user_email'] = email
            session['user_name'] = email.split('@')[0]
            return jsonify({
                'success': True,
                'message': '✅ Inicio de sesión exitoso',
                'user': {
                    'email': email,
                    'name': email.split('@')[0]
                }
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': '❌ Correo y contraseña son requeridos'
            }), 400
    
    @app.route('/api/registro', methods=['POST', 'OPTIONS'])
    def api_registro():
        """Registro de usuarios - API"""
        if request.method == 'OPTIONS':
            return '', 200
            
        data = request.get_json()
        nombre = data.get('nombre')
        email = data.get('email')
        telefono = data.get('telefono')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        
        if not all([nombre, email, telefono, password, confirm_password]):
            return jsonify({
                'success': False,
                'message': '❌ Todos los campos son obligatorios'
            }), 400
        elif password != confirm_password:
            return jsonify({
                'success': False,
                'message': '❌ Las contraseñas no coinciden'
            }), 400
        elif len(password) < 6:
            return jsonify({
                'success': False,
                'message': '❌ La contraseña debe tener al menos 6 caracteres'
            }), 400
        else:
            return jsonify({
                'success': True,
                'message': '✅ Registro exitoso. Por favor inicia sesión'
            }), 201
    
    @app.route('/api/logout', methods=['POST', 'OPTIONS'])
    def api_logout():
        """Cerrar sesión - API"""
        if request.method == 'OPTIONS':
            return '', 200
        session.clear()
        return jsonify({
            'success': True,
            'message': '✅ Sesión cerrada exitosamente'
        }), 200
    
    @app.route('/api/session', methods=['GET'])
    def api_check_session():
        """Verificar si hay sesión activa"""
        if 'user_email' in session:
            return jsonify({
                'isLoggedIn': True,
                'user': {
                    'email': session['user_email'],
                    'name': session['user_name']
                }
            }), 200
        else:
            return jsonify({
                'isLoggedIn': False
            }), 200
    
    # ==================== SERVICIOS ====================
    
    @app.route('/api/servicios', methods=['GET'])
    def api_get_servicios():
        """Obtener lista de servicios"""
        servicios = [
            {'id': 1, 'icono': 'fa-user-doctor', 'titulo': 'Atención Veterinaria', 'descripcion': 'Consultas con profesionales certificados.'},
            {'id': 2, 'icono': 'fa-syringe', 'titulo': 'Vacunación', 'descripcion': 'Control y programación de vacunas.'},
            {'id': 3, 'icono': 'fa-notes-medical', 'titulo': 'Historial Médico', 'descripcion': 'Registro completo de cada mascota.'},
            {'id': 4, 'icono': 'fa-house', 'titulo': 'Cuidado a Domicilio', 'descripcion': 'Cuidadores capacitados.'},
            {'id': 5, 'icono': 'fa-location-dot', 'titulo': 'Seguimiento', 'descripcion': 'Monitoreo constante de la atención.'}
        ]
        return jsonify({'success': True, 'servicios': servicios}), 200
    
    # ==================== CITAS ====================
    
    @app.route('/api/citas', methods=['GET'])
    def api_get_citas():
        """Obtener citas del usuario"""
        if 'user_email' not in session:
            return jsonify({'success': False, 'message': '⚠️ Debes iniciar sesión'}), 401
        
        citas = [
            {'id': 1, 'mascota': 'Firulais', 'fecha': '2026-01-20', 'hora': '10:00', 'motivo': 'Vacunación anual', 'estado': 'pendiente'},
            {'id': 2, 'mascota': 'Luna', 'fecha': '2026-01-15', 'hora': '14:30', 'motivo': 'Consulta general', 'estado': 'completada'}
        ]
        return jsonify({'success': True, 'citas': citas}), 200
    
    @app.route('/api/citas', methods=['POST', 'OPTIONS'])
    def api_crear_cita():
        """Crear una nueva cita"""
        if request.method == 'OPTIONS':
            return '', 200
        if 'user_email' not in session:
            return jsonify({'success': False, 'message': '⚠️ Debes iniciar sesión'}), 401
        
        data = request.get_json()
        mascota = data.get('mascota')
        fecha = data.get('fecha')
        hora = data.get('hora')
        motivo = data.get('motivo')
        
        if not all([mascota, fecha, hora, motivo]):
            return jsonify({'success': False, 'message': '❌ Todos los campos son obligatorios'}), 400
        
        return jsonify({
            'success': True,
            'message': '✅ Cita agendada exitosamente',
            'cita': {'id': 3, 'mascota': mascota, 'fecha': fecha, 'hora': hora, 'motivo': motivo, 'estado': 'pendiente'}
        }), 201
    
    # ==================== CUIDADORES ====================
    
    @app.route('/api/cuidadores', methods=['GET'])
    def api_get_cuidadores():
        """Obtener lista de cuidadores disponibles"""
        if 'user_email' not in session:
            return jsonify({'success': False, 'message': '⚠️ Debes iniciar sesión'}), 401
        
        cuidadores = [
            {'id': 1, 'nombre': 'María González', 'experiencia': '5 años', 'calificacion': 4.8, 'disponible': True, 'telefono': '3001234567', 'ciudad': 'Bogotá'},
            {'id': 2, 'nombre': 'Carlos Rodríguez', 'experiencia': '3 años', 'calificacion': 4.5, 'disponible': True, 'telefono': '3007654321', 'ciudad': 'Medellín'},
            {'id': 3, 'nombre': 'Ana Martínez', 'experiencia': '7 años', 'calificacion': 4.9, 'disponible': False, 'telefono': '3012345678', 'ciudad': 'Bogotá'}
        ]
        return jsonify({'success': True, 'cuidadores': cuidadores}), 200
    
    # ==================== MASCOTAS ====================
    
    @app.route('/api/mascotas', methods=['GET'])
    def api_get_mascotas():
        """Obtener mascotas del usuario"""
        if 'user_email' not in session:
            return jsonify({'success': False, 'message': '⚠️ Debes iniciar sesión'}), 401
        
        mascotas = [
            {'id': 1, 'nombre': 'Firulais', 'especie': 'Perro', 'raza': 'Labrador', 'edad': 3, 'peso': 25},
            {'id': 2, 'nombre': 'Luna', 'especie': 'Gato', 'raza': 'Siamés', 'edad': 2, 'peso': 4}
        ]
        return jsonify({'success': True, 'mascotas': mascotas}), 200
    
    @app.route('/api/mascotas', methods=['POST', 'OPTIONS'])
    def api_crear_mascota():
        """Registrar una nueva mascota"""
        if request.method == 'OPTIONS':
            return '', 200
        if 'user_email' not in session:
            return jsonify({'success': False, 'message': '⚠️ Debes iniciar sesión'}), 401
        
        data = request.get_json()
        nombre = data.get('nombre')
        especie = data.get('especie')
        raza = data.get('raza')
        edad = data.get('edad')
        peso = data.get('peso')
        
        if not all([nombre, especie, raza, edad]):
            return jsonify({'success': False, 'message': '❌ Nombre, especie, raza y edad son obligatorios'}), 400
        
        return jsonify({
            'success': True,
            'message': '✅ Mascota registrada exitosamente',
            'mascota': {'id': 3, 'nombre': nombre, 'especie': especie, 'raza': raza, 'edad': edad, 'peso': peso}
        }), 201
    
    # ==================== CONTACTO ====================
    
    @app.route('/api/contacto', methods=['POST', 'OPTIONS'])
    def api_contacto():
        """Enviar mensaje de contacto"""
        if request.method == 'OPTIONS':
            return '', 200
        data = request.get_json()
        nombre = data.get('nombre')
        email = data.get('email')
        mensaje = data.get('mensaje')
        
        if all([nombre, email, mensaje]):
            return jsonify({'success': True, 'message': '✅ Mensaje enviado exitosamente'}), 200
        else:
            return jsonify({'success': False, 'message': '❌ Todos los campos son obligatorios'}), 400

if __name__ == '__main__':
    app = create_app('development')
    app.run(host='127.0.0.1', port=5000, debug=True)