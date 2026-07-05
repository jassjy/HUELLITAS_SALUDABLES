let currentUser = null;

function showFlash(message, type = 'success') {
    const container = document.getElementById('flashMessages');
    const flash = document.createElement('div');
    flash.className = `flash-message flash-${type}`;
    flash.innerHTML = message;
    container.appendChild(flash);
    setTimeout(() => { flash.style.opacity = '0'; setTimeout(() => flash.remove(), 300); }, 3000);
}

function updateAuthButtons() {
    const authContainer = document.getElementById('authButtons');
    if (currentUser) {
        authContainer.innerHTML = `
            <li><a href="#" style="color:#4CAF50;">👤 ${currentUser.name}</a></li>
            <li><a href="#" onclick="cerrarSesion()" class="btn-menu">Cerrar Sesión</a></li>
        `;
    } else {
        authContainer.innerHTML = `
            <li><a href="#" onclick="showLoginForm()">Iniciar Sesión</a></li>
            <li><a href="#" onclick="showRegistroForm()" class="btn-menu">Registrarse</a></li>
        `;
    }
}

async function verificarSesion() {
    const result = await checkSession();
    currentUser = result.isLoggedIn ? result.user : null;
    updateAuthButtons();
}

async function cerrarSesion() {
    const result = await logout();
    if (result.success) {
        currentUser = null;
        updateAuthButtons();
        showFlash(result.message, 'success');
        showSection('inicio');
    }
}

function checkAuthAndShow(section) {
    if (currentUser) showSection(section);
    else showFlash('⚠️ Debes iniciar sesión', 'warning');
}

async function showLoginForm() {
    document.getElementById('mainContent').innerHTML = `
        <div class="form-container">
            <div class="formulario">
                <h2>🐾 Iniciar Sesión</h2>
                <input type="email" id="loginEmail" placeholder="Correo electrónico" required>
                <input type="password" id="loginPassword" placeholder="Contraseña" required>
                <button onclick="procesarLogin()">Iniciar Sesión</button>
                <a href="#" class="link" onclick="showRegistroForm()">¿No tienes cuenta? Regístrate</a>
            </div>
        </div>
    `;
}

async function procesarLogin() {
    const result = await login(document.getElementById('loginEmail').value, document.getElementById('loginPassword').value);
    if (result.success) {
        currentUser = result.user;
        updateAuthButtons();
        showFlash(result.message, 'success');
        showSection('inicio');
    } else showFlash(result.message, 'error');
}

async function showRegistroForm() {
    document.getElementById('mainContent').innerHTML = `
        <div class="form-container">
            <div class="formulario">
                <h2>🐾 Crear Cuenta</h2>
                <input type="text" id="regNombre" placeholder="Nombre completo" required>
                <input type="email" id="regEmail" placeholder="Correo electrónico" required>
                <input type="tel" id="regTelefono" placeholder="Teléfono" required>
                <input type="password" id="regPassword" placeholder="Contraseña" required>
                <input type="password" id="regConfirmPassword" placeholder="Confirmar contraseña" required>
                <button onclick="procesarRegistro()">Registrarse</button>
                <a href="#" class="link" onclick="showLoginForm()">¿Ya tienes cuenta? Inicia sesión</a>
            </div>
        </div>
    `;
}

async function procesarRegistro() {
    const result = await registro(
        document.getElementById('regNombre').value,
        document.getElementById('regEmail').value,
        document.getElementById('regTelefono').value,
        document.getElementById('regPassword').value,
        document.getElementById('regConfirmPassword').value
    );
    if (result.success) { showFlash(result.message, 'success'); showLoginForm(); }
    else showFlash(result.message, 'error');
}

async function showSection(section) {
    const main = document.getElementById('mainContent');
    if (section === 'inicio') {
        main.innerHTML = `
            <section class="hero">
                <div class="hero-text"><h1>Bienvenido a Huellitas Saludables</h1><p>Cuidamos a tu mascota cuando más lo necesita</p>
                <div><button class="btn" onclick="checkAuthAndShow('citas')">📅 Agendar Cita</button><button class="btn btn-secundario" onclick="checkAuthAndShow('cuidadores')">🏠 Solicitar Cuidador</button></div></div>
                <div class="hero-img"><img src="img/HueLLitas-Saludables.jpg" alt="Mascotas felices"></div>
            </section>
            <section class="servicios" id="servicios"><h2>Nuestros Servicios</h2><div id="serviciosList" class="cards"></div></section>
            <section class="funciona"><h2>¿Cómo funciona?</h2><div class="pasos"><div class="paso"><span>1</span><p>Registra tu cuenta</p></div><div class="paso"><span>2</span><p>Registra tu mascota</p></div><div class="paso"><span>3</span><p>Agenda una cita</p></div><div class="paso"><span>4</span><p>Recibe seguimiento</p></div></div></section>
        `;
        cargarServicios();
    }
    else if (section === 'servicios') {
        main.innerHTML = `<section class="servicios" style="padding-top:6rem"><h2>Nuestros Servicios</h2><div id="serviciosList" class="cards"></div></section>`;
        cargarServicios();
    }
    else if (section === 'citas') await mostrarCitas();
    else if (section === 'cuidadores') await mostrarCuidadores();
    else if (section === 'mascotas') await mostrarMascotas();
    else if (section === 'contacto') mostrarContacto();
}

async function cargarServicios() {
    const result = await getServicios();
    if (result.success) {
        document.getElementById('serviciosList').innerHTML = result.servicios.map(s => `
            <div class="card"><i class="fa-solid ${s.icono}"></i><h3>${s.titulo}</h3><p>${s.descripcion}</p></div>
        `).join('');
    }
}

async function mostrarCitas() {
    const citasResult = await getCitas();
    document.getElementById('mainContent').innerHTML = `
        <div class="form-container" style="flex-direction:column">
            <div class="formulario"><h2>📅 Agendar Nueva Cita</h2>
                <input type="text" id="citaMascota" placeholder="Nombre de la mascota">
                <input type="date" id="citaFecha"><input type="time" id="citaHora">
                <textarea id="citaMotivo" placeholder="Motivo de la cita"></textarea>
                <button onclick="agendarCita()">Agendar Cita</button>
            </div>
            <div class="tabla-container"><h3>📋 Mis Citas</h3><table class="tabla"><thead><tr><th>Mascota</th><th>Fecha</th><th>Hora</th><th>Motivo</th><th>Estado</th></tr></thead><tbody id="citasLista"></tbody></table></div>
        </div>
    `;
    if (citasResult.success && citasResult.citas) {
        document.getElementById('citasLista').innerHTML = citasResult.citas.map(c => `
            <tr><td>${c.mascota}</td><td>${c.fecha}</td><td>${c.hora}</td><td>${c.motivo}</td><td>${c.estado}</td></tr>
        `).join('');
    }
}

async function agendarCita() {
    const result = await crearCita({
        mascota: document.getElementById('citaMascota').value,
        fecha: document.getElementById('citaFecha').value,
        hora: document.getElementById('citaHora').value,
        motivo: document.getElementById('citaMotivo').value
    });
    showFlash(result.message, result.success ? 'success' : 'error');
    if (result.success) mostrarCitas();
}

async function mostrarCuidadores() {
    const result = await getCuidadores();
    document.getElementById('mainContent').innerHTML = `
        <div class="form-container" style="flex-direction:column"><h2>🐕 Cuidadores Disponibles</h2>
        <div id="cuidadoresList" class="cuidadores-grid"></div></div>
    `;
    if (result.success) {
        document.getElementById('cuidadoresList').innerHTML = result.cuidadores.map(c => `
            <div class="cuidador-card"><h3>${c.nombre}</h3><p>📍 ${c.ciudad}</p><p>⭐ ${c.calificacion} ★</p><p>📅 ${c.experiencia} de experiencia</p><p>📞 ${c.telefono}</p><p class="${c.disponible ? 'disponible' : 'no-disponible'}">${c.disponible ? '✅ Disponible' : '❌ No disponible'}</p></div>
        `).join('');
    }
}

async function mostrarMascotas() {
    const result = await getMascotas();
    document.getElementById('mainContent').innerHTML = `
        <div class="form-container" style="flex-direction:column">
            <div class="formulario"><h2>🐾 Registrar Mascota</h2>
                <input type="text" id="mascotaNombre" placeholder="Nombre"><select id="mascotaEspecie"><option value="Perro">Perro</option><option value="Gato">Gato</option></select>
                <input type="text" id="mascotaRaza" placeholder="Raza"><input type="number" id="mascotaEdad" placeholder="Edad"><input type="number" id="mascotaPeso" placeholder="Peso (kg)">
                <button onclick="registrarMascota()">Registrar Mascota</button>
            </div>
            <div class="tabla-container"><h3>📋 Mis Mascotas</h3><table class="tabla"><thead><tr><th>Nombre</th><th>Especie</th><th>Raza</th><th>Edad</th><th>Peso</th></tr></thead><tbody id="mascotasLista"></tbody></table></div>
        </div>
    `;
    if (result.success) {
        document.getElementById('mascotasLista').innerHTML = result.mascotas.map(m => `
            <tr><td>${m.nombre}</td><td>${m.especie}</td><td>${m.raza}</td><td>${m.edad} años</td><td>${m.peso || '-'} kg</td></tr>
        `).join('');
    }
}

async function registrarMascota() {
    const result = await crearMascota({
        nombre: document.getElementById('mascotaNombre').value,
        especie: document.getElementById('mascotaEspecie').value,
        raza: document.getElementById('mascotaRaza').value,
        edad: parseInt(document.getElementById('mascotaEdad').value),
        peso: parseFloat(document.getElementById('mascotaPeso').value) || null
    });
    showFlash(result.message, result.success ? 'success' : 'error');
    if (result.success) mostrarMascotas();
}

function mostrarContacto() {
    document.getElementById('mainContent').innerHTML = `
        <div class="form-container"><div class="formulario"><h2>📧 Contáctanos</h2>
            <input type="text" id="contactoNombre" placeholder="Nombre completo"><input type="email" id="contactoEmail" placeholder="Correo electrónico">
            <textarea id="contactoMensaje" placeholder="Escribe tu mensaje..."></textarea><button onclick="enviarContacto()">Enviar Mensaje</button>
        </div></div>
    `;
}

async function enviarContacto() {
    const result = await enviarContacto({
        nombre: document.getElementById('contactoNombre').value,
        email: document.getElementById('contactoEmail').value,
        mensaje: document.getElementById('contactoMensaje').value
    });
    showFlash(result.message, result.success ? 'success' : 'error');
    if (result.success) showSection('inicio');
}

// Inicializar
verificarSesion();
showSection('inicio');