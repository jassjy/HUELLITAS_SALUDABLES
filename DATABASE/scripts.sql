-- Crear la base de datos (opcional, ajusta el nombre según prefieras)
CREATE DATABASE IF NOT EXISTS mascotas_servicios;
USE mascotas_servicios;

-- Tabla: ROLES
CREATE TABLE roles (
    id_roles INT AUTO_INCREMENT PRIMARY KEY,
    nombre_usuario VARCHAR(100) NOT NULL,
    contraseña VARCHAR(255) NOT NULL,
    email_usuario VARCHAR(150) NOT NULL UNIQUE,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    dirección VARCHAR(255),
    foto_perfil VARCHAR(300),
    perfil ENUM('dueno', 'veterinario', 'cuidador', 'adoptivo') NOT NULL,
    telefono VARCHAR(20),
    proveedor VARCHAR(20)
);

-- Tabla: NOTIFICACION
CREATE TABLE notificacion (
    id_notificacion INT AUTO_INCREMENT PRIMARY KEY,
    id_roles INT NOT NULL,
    mensaje VARCHAR(500) NOT NULL,
    tipo ENUM('SERVICIO', 'Tips') NOT NULL,
    fecha_envio DATETIME DEFAULT CURRENT_TIMESTAMP,
    canal_envio VARCHAR(50),
    FOREIGN KEY (id_roles) REFERENCES role(id_roles) ON DELETE CASCADE
);

-- Tabla: MASCOTA
CREATE TABLE mascota (
    id_mascota INT AUTO_INCREMENT PRIMARY KEY,
    id_dueno INT NOT NULL,
    nombre VARCHAR(80) NOT NULL,
    especie VARCHAR(80) NOT NULL,
    raza VARCHAR(80),
    peso_kg DECIMAL(5,2),
    fecha_nacimiento DATE,
    foto_mascota VARCHAR(300),
    -- Edad se calcula, no se almacena directamente
    FOREIGN KEY (id_dueno) REFERENCES role(id_roles) ON DELETE CASCADE
);

-- Tabla: SERVICIO
CREATE TABLE servicio (
    id_servicio INT AUTO_INCREMENT PRIMARY KEY,
    id_roles_proveedor INT NOT NULL,
    id_mascota INT NOT NULL,
    fecha DATETIME NOT NULL,
    tipo_servicio ENUM('veterinario', 'cuidador', 'banco') NOT NULL,
    notas TEXT,
    costo DECIMAL(10,2),
    estado ENUM('activo', 'finalizado', 'cancelado') DEFAULT 'activo',
    duracion TIME, -- Corregido: /duración_time -> duracion TIME
    FOREIGN KEY (id_roles_proveedor) REFERENCES role(id_roles),
    FOREIGN KEY (id_mascota) REFERENCES mascota(id_mascota)
);

-- Tabla: CALIFICACION (ajustado para que tenga sentido)
CREATE TABLE calificacion (
    id_calificacion INT AUTO_INCREMENT PRIMARY KEY,
    id_servicio INT NOT NULL,
    id_roles_usuario INT NOT NULL, -- Usuario que califica
    fecha DATE DEFAULT (CURRENT_DATE),
    puntuacion TINYINT CHECK (puntuacion BETWEEN 1 AND 5),
    tipo_servicio_calificado VARCHAR(50),
    comentario TEXT,
    FOREIGN KEY (id_servicio) REFERENCES servicio(id_servicio) ON DELETE CASCADE,
    FOREIGN KEY (id_roles_usuario) REFERENCES role(id_roles)
);

-- Tabla: DISPONIBILIDAD (para proveedores)
CREATE TABLE disponibilidad (
    id_disponibilidad INT AUTO_INCREMENT PRIMARY KEY,
    id_roles_proveedor INT NOT NULL,
    fecha DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    estado ENUM('disponible', 'ocupado') DEFAULT 'disponible',
    -- horas_totales no se almacena, se puede calcular como timediff(hora_fin, hora_inicio)
    FOREIGN KEY (id_roles_proveedor) REFERENCES role(id_roles) ON DELETE CASCADE
);

-- Ejemplo de inserción de datos de prueba (opcional)
INSERT INTO roles (nombre_usuario, contraseña, email_usuario, perfil, telefono)
VALUES 
('juan_perez', 'hash123', 'juan@mail.com', 'dueno', '123456789'),
('vet_ana', 'hash456', 'ana@vet.com', 'veterinario', '987654321');

INSERT INTO mascota (id_dueno, nombre, especie, raza, peso_kg, fecha_nacimiento)
VALUES (1, 'Rex', 'Perro', 'Labrador', 25.50, '2020-05-10');

INSERT INTO disponibilidad (id_roles_proveedor, fecha, hora_inicio, hora_fin)
VALUES (2, '2026-06-15', '09:00:00', '17:00:00');