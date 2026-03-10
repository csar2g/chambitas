CREATE DATABASE chambitas;
USE chambitas;

-- =========================
-- Usuario
-- =========================
CREATE TABLE Usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50),
    fechaNacimiento DATE,
    ubicacion VARCHAR(30),
    correo VARCHAR(100) UNIQUE,
    contrasena VARCHAR(255),
    estado ENUM('activo','inactivo') DEFAULT 'activo',
    created_at DATETIME,
    updated_at DATETIME
);

-- =========================
-- Perfil (1:1 con Usuario). Incluye datos de contacto y enlaces.
-- =========================
CREATE TABLE Perfil (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT UNIQUE,
    descripcion TEXT,
    numero_tel VARCHAR(20),
    whatsapp VARCHAR(20),
    FOREIGN KEY (usuario_id) REFERENCES Usuario(id)
        ON DELETE CASCADE
);

-- =========================
-- Link (relacionado a Perfil)
-- =========================
CREATE TABLE Link (
    id INT AUTO_INCREMENT PRIMARY KEY,
    perfil_id INT,
    url VARCHAR(255),
    FOREIGN KEY (perfil_id) REFERENCES Perfil(id)
        ON DELETE CASCADE
);

-- =========================
-- Publicacion
-- =========================
CREATE TABLE Publicacion (
    publicacion_id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    img VARCHAR(255),
    descripcion TEXT,
    created_at DATETIME,
    updated_at DATETIME,
    FOREIGN KEY (usuario_id) REFERENCES Usuario(id)
        ON DELETE CASCADE
);

-- =========================
-- Reaccion
-- =========================
CREATE TABLE Reaccion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    publicacion_id INT,
    usuario_id INT,
    created_at DATETIME,
    FOREIGN KEY (publicacion_id) REFERENCES Publicacion(publicacion_id)
        ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES Usuario(id)
        ON DELETE CASCADE
);

-- =========================
-- Comentario
-- =========================
CREATE TABLE Comentario (
    comentario_id INT AUTO_INCREMENT PRIMARY KEY,
    publicacion_id INT,
    usuario_id INT,
    created_at DATETIME,
    FOREIGN KEY (publicacion_id) REFERENCES Publicacion(publicacion_id)
        ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES Usuario(id)
        ON DELETE CASCADE
);

-- =========================
-- Aptitud
-- =========================
CREATE TABLE Aptitud (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(40)
);

-- =========================
-- UsuarioAptitud (N:M)
-- =========================
CREATE TABLE UsuarioAptitud (
    usuario_id INT,
    aptitud_id INT,
    PRIMARY KEY (usuario_id, aptitud_id),
    FOREIGN KEY (usuario_id) REFERENCES Usuario(id)
        ON DELETE CASCADE,
    FOREIGN KEY (aptitud_id) REFERENCES Aptitud(id)
        ON DELETE CASCADE
);

-- =========================
-- Interes
-- =========================
CREATE TABLE Interes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(30)
);

-- =========================
-- UsuarioInteres (N:M)
-- =========================
CREATE TABLE UsuarioInteres (
    id_interes INT,
    id_usuario INT,
    PRIMARY KEY (id_interes, id_usuario),
    FOREIGN KEY (id_interes) REFERENCES Interes(id)
        ON DELETE CASCADE,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id)
        ON DELETE CASCADE
);

-- =========================
-- Recomendaciones
-- =========================
CREATE TABLE Recomendaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_emisor_id INT,
    usuario_receptor_id INT,
    contenido TEXT,
    created_at DATETIME,
    updated_at DATETIME,
    FOREIGN KEY (usuario_emisor_id) REFERENCES Usuario(id),
    FOREIGN KEY (usuario_receptor_id) REFERENCES Usuario(id)
);

-- =========================
-- Conversacion
-- =========================
CREATE TABLE Conversacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_emisor_id INT,
    usuario_receptor_id INT,
    created_at DATETIME,
    FOREIGN KEY (usuario_emisor_id) REFERENCES Usuario(id),
    FOREIGN KEY (usuario_receptor_id) REFERENCES Usuario(id)
);

-- =========================
-- Mensaje
-- =========================
CREATE TABLE Mensaje (
    id INT AUTO_INCREMENT PRIMARY KEY,
    conversacion_id INT,
    usuario_emisor_id INT,
    contenido TEXT,
    created_at DATETIME,
    FOREIGN KEY (conversacion_id) REFERENCES Conversacion(id)
        ON DELETE CASCADE,
    FOREIGN KEY (usuario_emisor_id) REFERENCES Usuario(id)
);
