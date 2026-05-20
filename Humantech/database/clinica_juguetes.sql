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

CREATE TABLE categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    slug VARCHAR(100) NOT NULL UNIQUE,
    activa BOOLEAN NOT NULL DEFAULT TRUE,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE juguetes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo_barras VARCHAR(80) NOT NULL UNIQUE,
    nombre VARCHAR(120) NOT NULL,
    categoria_id INT NOT NULL,
    descripcion TEXT,

    donante_id INT NULL,
    donante_nombre VARCHAR(120) NOT NULL,
    donante_correo VARCHAR(150) NOT NULL,
    donante_telefono VARCHAR(30) NULL,

    estado_actual ENUM(
        'registrado',
        'en_revision',
        'en_reparacion',
        'reparado',
        'listo_para_entrega',
        'entregado',
        'descartado'
    ) NOT NULL DEFAULT 'registrado',

    fecha_recepcion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_juguetes_categoria
        FOREIGN KEY (categoria_id)
        REFERENCES categorias(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_juguetes_donante
        FOREIGN KEY (donante_id)
        REFERENCES usuarios(id)
        ON DELETE SET NULL
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

/* SEEDS */

INSERT INTO usuarios (
      id, cedula, primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, contacto, clave, rol
    ) VALUES
    (1, '111111', 'Tester', NULL, 'Admin', NULL, 'admin@test.com', 'tester', 'admin'),
    (2, '222222', 'Laura', 'Marcela', 'Gómez', 'Ríos', 'laura@test.com', '123456', 'donante'),
    (3, '333333', 'Carlos', NULL, 'Pérez', 'Mora', 'carlos@test.com', '123456', 'donante'),
    (4, '444444', 'Ana', 'María', 'Torres', 'Díaz', 'ana@test.com', '123456', 'donante'),
    (5, '555555', 'Miguel', NULL, 'Ramírez', 'Castro', 'miguel@test.com', '123456', 'donante'),
    (6, '666666', 'Sofía', 'Isabel', 'Moreno', 'Vargas', 'sofia@test.com', '123456', 'donante'),
    (7, '777777', 'Daniel', NULL, 'Campos', 'Ortiz', 'daniel@test.com', '123456', 'donante'),
    (8, '888888', 'Valentina', NULL, 'Herrera', 'López', 'valentina@test.com', '123456', 'donante'),
    (9, '999999', 'Andrés', 'Felipe', 'Ruiz', 'Salazar', 'andres@test.com', '123456', 'donante'),
    (10, '101010', 'Camila', NULL, 'Navarro', 'Peña', 'camila@test.com', '123456', 'donante');

INSERT INTO beneficiarios (
      id, nombre, documento, edad, institucion, contacto, observaciones
    ) VALUES
    (1, 'Juan Esteban', 'B001', 7, 'Fundación Semillas', '3000000001', 'Beneficiario de prueba'),
    (2, 'María José', 'B002', 8, 'Fundación Semillas', '3000000002', 'Beneficiaria de prueba'),
    (3, 'Samuel David', 'B003', 6, 'Hogar Infantil Luz', '3000000003', 'Beneficiario de prueba'),
    (4, 'Valeria Sofía', 'B004', 9, 'Hogar Infantil Luz', '3000000004', 'Beneficiaria de prueba'),
    (5, 'Nicolás Andrés', 'B005', 10, 'Comedor Comunitario Norte', '3000000005', 'Beneficiario de prueba'),
    (6, 'Isabella', 'B006', 5, 'Comedor Comunitario Norte', '3000000006', 'Beneficiaria de prueba'),
    (7, 'Dylan Mateo', 'B007', 11, 'Fundación Manos Amigas', '3000000007', 'Beneficiario de prueba'),
    (8, 'Luciana', 'B008', 7, 'Fundación Manos Amigas', '3000000008', 'Beneficiaria de prueba'),
    (9, 'Emmanuel', 'B009', 8, 'Colegio Comunitario Sur', '3000000009', 'Beneficiario de prueba'),
    (10, 'Sara Valentina', 'B010', 6, 'Colegio Comunitario Sur', '3000000010', 'Beneficiaria de prueba');

INSERT INTO categorias (
      id, nombre, slug, activa
    ) VALUES
    (1, 'Hot Wheels', 'hotwheels', TRUE),
    (2, 'Camiones', 'camiones', TRUE),
    (3, 'Vehículos a control remoto', 'vehiculos_control_remoto', TRUE),
    (4, 'Muñeca', 'muneca', TRUE),
    (5, 'Bebé', 'bebe', TRUE),
    (6, 'Peluches', 'peluches', TRUE),
    (7, 'Fútbol', 'futbol', TRUE),
    (8, 'Baloncesto', 'baloncesto', TRUE),
    (9, 'Voleibol', 'voleibol', TRUE),
    (10, 'Juegos de mesa', 'juegos_de_mesa', TRUE),
    (11, 'Inflables', 'inflables', TRUE),
    (12, 'Otros', 'otros', TRUE);

INSERT INTO juguetes (
    id,
    codigo_barras,
    nombre,
    categoria_id,
    descripcion,
    donante_id,
    donante_nombre,
    donante_correo,
    donante_telefono,
    estado_actual,
    fecha_recepcion
) VALUES
(
    1,
    'JUG-000001',
    'Carro Hot Wheels',
    1,
    'Carro pequeño en buen estado, requiere limpieza superficial.',
    NULL,
    'Laura Gómez',
    'laura.gomez@test.com',
    '3001111111',
    'registrado',
    NOW()
),
(
    2,
    'JUG-000002',
    'Muñeca de colección',
    4,
    'Muñeca con vestido rosado, tiene marcas de uso.',
    NULL,
    'Carlos Pérez',
    'carlos.perez@test.com',
    '3002222222',
    'en_revision',
    NOW()
),
(
    3,
    'JUG-000003',
    'Balón de fútbol',
    7,
    'Balón usado, necesita revisión de presión y limpieza.',
    NULL,
    'Ana Torres',
    'ana.torres@test.com',
    NULL,
    'en_reparacion',
    NOW()
),
(
    4,
    'JUG-000004',
    'Camión plástico',
    2,
    'Camión grande de plástico, reparado y entregado durante jornada social.',
    NULL,
    'Miguel Ramírez',
    'miguel.ramirez@test.com',
    '3004444444',
    'entregado',
    NOW()
),
(
    5,
    'JUG-000005',
    'Peluche de oso',
    6,
    'Peluche limpio, suave y en buen estado.',
    NULL,
    'Sofía Moreno',
    'sofia.moreno@test.com',
    '3005555555',
    'listo_para_entrega',
    NOW()
),
(
    6,
    'JUG-000006',
    'Juego de memoria',
    10,
    'Juego de memoria incompleto, se descartó por piezas faltantes.',
    NULL,
    'Daniel Campos',
    'daniel.campos@test.com',
    NULL,
    'descartado',
    NOW()
),
(
    7,
    'JUG-000007',
    'Vehículo a control remoto',
    3,
    'Carro a control remoto sin batería, requiere reparación electrónica.',
    NULL,
    'Valentina Herrera',
    'valentina.herrera@test.com',
    '3007777777',
    'en_reparacion',
    NOW()
),
(
    8,
    'JUG-000008',
    'Balón de baloncesto',
    8,
    'Balón con poco aire, pendiente revisión.',
    NULL,
    'Andrés Ruiz',
    'andres.ruiz@test.com',
    '3008888888',
    'registrado',
    NOW()
),
(
    9,
    'JUG-000009',
    'Muñeco bebé',
    5,
    'Muñeco bebé con ropa azul, entregado en jornada de prueba.',
    NULL,
    'Camila Navarro',
    'camila.navarro@test.com',
    '3009999999',
    'entregado',
    NOW()
),
(
    10,
    'JUG-000010',
    'Balón inflable',
    11,
    'Balón inflable colorido, listo para próxima jornada.',
    NULL,
    'Mariana López',
    'mariana.lopez@test.com',
    NULL,
    'listo_para_entrega',
    NOW()
);

INSERT INTO historial_estados_juguete (
      juguete_id, estado_anterior, estado_nuevo, observacion, usuario_id
    ) VALUES
    (1, NULL, 'registrado', 'Juguete registrado en el sistema.', 1),
    (2, NULL, 'registrado', 'Juguete registrado en el sistema.', 1),
    (2, 'registrado', 'en_revision', 'Se inició revisión física del juguete.', 1),
    (3, NULL, 'registrado', 'Juguete registrado en el sistema.', 1),
    (3, 'registrado', 'en_revision', 'Se detectó desgaste general.', 1),
    (3, 'en_revision', 'en_reparacion', 'Requiere limpieza y reparación menor.', 1),
    (4, NULL, 'registrado', 'Juguete registrado en el sistema.', 1),
    (4, 'registrado', 'reparado', 'Juguete reparado y funcional.', 1),
    (5, NULL, 'registrado', 'Juguete registrado en el sistema.', 1),
    (5, 'registrado', 'listo_para_entrega', 'Juguete limpio y listo para entregar.', 1);

INSERT INTO entregas (
      id, juguete_id, beneficiario_id, entregado_por_id, lugar_entrega, fecha_entrega, observaciones
    ) VALUES
    (1, 9, 1, 1, 'Fundación Semillas', NOW(), 'Entrega realizada correctamente.'),
    (2, 4, 2, 1, 'Hogar Infantil Luz', NOW(), 'Entrega simbólica de prueba.'),
    (3, 5, 3, 1, 'Comedor Comunitario Norte', NOW(), 'Pendiente confirmación familiar.'),
    (4, 10, 4, 1, 'Fundación Manos Amigas', NOW(), 'Entrega agendada.'),
    (5, 1, 5, 1, 'Colegio Comunitario Sur', NOW(), 'Registro de prueba.'),
    (6, 2, 6, 1, 'Fundación Semillas', NOW(), 'Registro de prueba.'),
    (7, 3, 7, 1, 'Hogar Infantil Luz', NOW(), 'Registro de prueba.'),
    (8, 6, 8, 1, 'Comedor Comunitario Norte', NOW(), 'Registro de prueba.'),
    (9, 7, 9, 1, 'Fundación Manos Amigas', NOW(), 'Registro de prueba.'),
    (10, 8, 10, 1, 'Colegio Comunitario Sur', NOW(), 'Registro de prueba.');