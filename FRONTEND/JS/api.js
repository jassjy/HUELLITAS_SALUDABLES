// Configuración de la API
const API_URL = 'http://127.0.0.1:5000/api';

async function apiRequest(endpoint, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include'
    };
    
    if (data) options.body = JSON.stringify(data);
    
    try {
        const response = await fetch(`${API_URL}${endpoint}`, options);
        return await response.json();
    } catch (error) {
        console.error('Error:', error);
        return { success: false, message: 'Error de conexión con el servidor' };
    }
}

// Funciones de la API
async function login(email, password) {
    return await apiRequest('/login', 'POST', { email, password });
}

async function registro(nombre, email, telefono, password, confirm_password) {
    return await apiRequest('/registro', 'POST', { 
        nombre, email, telefono, password, confirm_password 
    });
}

async function logout() {
    return await apiRequest('/logout', 'POST');
}

async function checkSession() {
    return await apiRequest('/session', 'GET');
}

async function getServicios() {
    return await apiRequest('/servicios', 'GET');
}

async function getCitas() {
    return await apiRequest('/citas', 'GET');
}
async function enviarMensajeContacto(datos) {
    try {
        const response = await fetch('/api/contacto', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(datos)
        });
        return await response.json();
    } catch (error) {
        console.error('Error:', error);
        return { success: false, message: 'Error de conexión' };
    }
}
async function crearCita(datos) {
    return await apiRequest('/citas', 'POST', datos);
}

async function getCuidadores() {
    return await apiRequest('/cuidadores', 'GET');
}

async function getMascotas() {
    return await apiRequest('/mascotas', 'GET');
}

async function crearMascota(datos) {
    return await apiRequest('/mascotas', 'POST', datos);
}

async function enviarContacto(datos) {
    return await apiRequest('/contacto', 'POST', datos);
}