"""
Punto de entrada principal de la API REST de Huellitas Saludables
"""

import sys
import os
import webbrowser
import threading
import time

backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from BACKEND.src.app import create_app

def open_browser():
    """Abrir el navegador después de un pequeño retraso"""
    time.sleep(1.5)
    webbrowser.open('http://127.0.0.1:5000')

def main():
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║     🐾  HUELLITAS SALUDABLES API REST v1.0.0  🐾        ║
    ║                                                          ║
    ║     API para gestión de mascotas, citas y cuidadores     ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    app = create_app('development')
    
    print(f"\n📋 Información de la API:")
    print(f"   • Aplicación: {app.config['APP_NAME']}")
    print(f"   • Versión: {app.config['APP_VERSION']}")
    print(f"   • Modo: {app.config.get('ENV', 'development').upper()}")
    print(f"   • Debug: {'✅ Activado' if app.config['DEBUG'] else '❌ Desactivado'}")
    print(f"\n🌐 API endpoints disponibles:")
    print(f"   • POST   /api/login")
    print(f"   • POST   /api/registro")
    print(f"   • POST   /api/logout")
    print(f"   • GET    /api/session")
    print(f"   • GET    /api/servicios")
    print(f"   • GET    /api/citas")
    print(f"   • POST   /api/citas")
    print(f"   • GET    /api/cuidadores")
    print(f"   • GET    /api/mascotas")
    print(f"   • POST   /api/mascotas")
    print(f"   • POST   /api/contacto")
    print(f"\n🚀 Servidor API: http://127.0.0.1:5000")
    print(f"📁 Frontend: Abre FRONTEND/index.html con Live Server")
    print(f"\n💡 Presiona CTRL+C para detener")
    print("═" * 58)
    
    try:
        app.run(host='127.0.0.1', port=5000, debug=True, threaded=True, use_reloader=False)
    except KeyboardInterrupt:
        print("\n\n👋 API detenida. ¡Gracias!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()