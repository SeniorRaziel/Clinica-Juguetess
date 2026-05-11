DROP DATABASE IF EXISTS clinica_juguetes;
CREATE DATABASE clinica_juguetes CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE clinica_juguetes;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cedula VARCHAR(20) NOT NULL UNIQUE,
    primer_nombre VARCHAR(80) NOT NULL,
    segundo_nombre VARCHAR(80),
    primer_apellido VARCHAR(80) NOT NULL,
    segundo_apellido VARCHAR(80),
    contacto VARCHAR(150) NOT NULL,
    clave VARCHAR(255) NOT NULL,
    rol ENUM('donante', 'admin') NOT NULL DEFAULT 'donante',
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE juguetes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(80) NOT NULL UNIQUE,
    codigo_barras VARCHAR(80) NOT NULL UNIQUE,
    nombre VARCHAR(120) NOT NULL,
    categoria VARCHAR(80) NOT NULL,
    descripcion TEXT,
    estado_actual ENUM(
        'registrado',
        'en_revision',
        'en_reparacion',
        'reparado',
        'listo_para_entrega',
        'entregado',
        'descartado'
    ) NOT NULL DEFAULT 'registrado',
    donante_id INT NOT NULL,
    fecha_recepcion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_juguetes_donante
        FOREIGN KEY (donante_id)
        REFERENCES usuarios(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

CREATE TABLE historial_estados_juguete (
    id INT AUTO_INCREMENT PRIMARY KEY,
    juguete_id INT NOT NULL,
    estado_anterior VARCHAR(50),
    estado_nuevo VARCHAR(50) NOT NULL,
    observacion TEXT,
    usuario_id INT NOT NULL,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_historial_juguete
        FOREIGN KEY (juguete_id)
        REFERENCES juguetes(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_historial_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

CREATE TABLE beneficiarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    documento VARCHAR(30),
    edad INT,
    institucion VARCHAR(150),
    contacto VARCHAR(150),
    observaciones TEXT,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE entregas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    juguete_id INT NOT NULL UNIQUE,
    beneficiario_id INT NOT NULL,
    entregado_por_id INT NOT NULL,
    lugar_entrega VARCHAR(150) NOT NULL,
    fecha_entrega TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    observaciones TEXT,

    CONSTRAINT fk_entregas_juguete
        FOREIGN KEY (juguete_id)
        REFERENCES juguetes(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_entregas_beneficiario
        FOREIGN KEY (beneficiario_id)
        REFERENCES beneficiarios(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_entregas_usuario
        FOREIGN KEY (entregado_por_id)
        REFERENCES usuarios(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

INSERT INTO usuarios (
    cedula,
    primer_nombre,
    primer_apellido,
    contacto,
    clave,
    rol
) VALUES (
    '123456789',
    'Admin',
    'Principal',
    'admin@test.com',
    '123456',
    'admin'
);

INSERT INTO beneficiarios (
    nombre,
    documento,
    edad,
    institucion,
    contacto,
    observaciones
) VALUES
('Niño beneficiario 1', '1001', 8, 'Fundación Semillas', '3000000001', 'Beneficiario de prueba'),
('Niña beneficiaria 2', '1002', 7, 'Fundación Semillas', '3000000002', 'Beneficiaria de prueba');
