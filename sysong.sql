CREATE DATABASE  IF NOT EXISTS `sysong` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `sysong`;
-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: sysong
-- ------------------------------------------------------
-- Server version	9.2.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `almacen`
--

DROP TABLE IF EXISTS `almacen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `almacen` (
  `id_almacen` int NOT NULL,
  `capacidad` int NOT NULL,
  `ubicacion` varchar(100) NOT NULL,
  `nombre_almacen` varchar(45) NOT NULL,
  `horario` enum('Mañana','Tarde','Noche') NOT NULL,
  `descripcion` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_almacen`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `almacen`
--

LOCK TABLES `almacen` WRITE;
/*!40000 ALTER TABLE `almacen` DISABLE KEYS */;
/*!40000 ALTER TABLE `almacen` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `almacen_suministros`
--

DROP TABLE IF EXISTS `almacen_suministros`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `almacen_suministros` (
  `id_suministro` int NOT NULL,
  `almacen_id` int NOT NULL,
  `producto_id` int NOT NULL,
  `stock_maximo` int NOT NULL,
  PRIMARY KEY (`id_suministro`),
  UNIQUE KEY `almacen_id_UNIQUE` (`almacen_id`),
  UNIQUE KEY `id_suministro_UNIQUE` (`id_suministro`),
  KEY `almacen_id_idx` (`almacen_id`),
  KEY `producto_id_suministros_idx` (`producto_id`),
  CONSTRAINT `almacen_id_suministros` FOREIGN KEY (`almacen_id`) REFERENCES `almacen` (`id_almacen`),
  CONSTRAINT `producto_id_suministros` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id_producto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `almacen_suministros`
--

LOCK TABLES `almacen_suministros` WRITE;
/*!40000 ALTER TABLE `almacen_suministros` DISABLE KEYS */;
/*!40000 ALTER TABLE `almacen_suministros` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `almacen_vehiculos`
--

DROP TABLE IF EXISTS `almacen_vehiculos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `almacen_vehiculos` (
  `id_almacen_vehiculos` int NOT NULL,
  `vehiculo_id` int NOT NULL,
  PRIMARY KEY (`id_almacen_vehiculos`),
  UNIQUE KEY `id_almacen_vehiculos_UNIQUE` (`id_almacen_vehiculos`),
  KEY `vehiculo_id_almacen_idx` (`vehiculo_id`),
  CONSTRAINT `vehiculo_id_almacen` FOREIGN KEY (`vehiculo_id`) REFERENCES `vehiculos` (`id_vehiculo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `almacen_vehiculos`
--

LOCK TABLES `almacen_vehiculos` WRITE;
/*!40000 ALTER TABLE `almacen_vehiculos` DISABLE KEYS */;
/*!40000 ALTER TABLE `almacen_vehiculos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `apoyos`
--

DROP TABLE IF EXISTS `apoyos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `apoyos` (
  `id_apoyo` int NOT NULL,
  `programa_id` int NOT NULL,
  `tipo_apoyo` varchar(100) DEFAULT NULL,
  `descripcion` text,
  `monto` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id_apoyo`),
  UNIQUE KEY `id_apoyo_UNIQUE` (`id_apoyo`),
  KEY `programa_id` (`programa_id`),
  CONSTRAINT `apoyos_ibfk_1` FOREIGN KEY (`programa_id`) REFERENCES `programas` (`id_programa`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apoyos`
--

LOCK TABLES `apoyos` WRITE;
/*!40000 ALTER TABLE `apoyos` DISABLE KEYS */;
/*!40000 ALTER TABLE `apoyos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `asignacion_logistica`
--

DROP TABLE IF EXISTS `asignacion_logistica`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `asignacion_logistica` (
  `id_asignacion` int NOT NULL,
  `vehiculo_id` int NOT NULL,
  `ruta_id` int NOT NULL,
  `personal_id` int NOT NULL,
  `fecha_asignacion` date NOT NULL,
  PRIMARY KEY (`id_asignacion`),
  UNIQUE KEY `id_asignacion_UNIQUE` (`id_asignacion`),
  UNIQUE KEY `vehiculo_id_UNIQUE` (`vehiculo_id`),
  UNIQUE KEY `ruta_id_UNIQUE` (`ruta_id`),
  KEY `fk_ruta_id_idx` (`ruta_id`),
  KEY `fk_personal_id_idx` (`personal_id`),
  KEY `fk_vehiculo_id_idx` (`vehiculo_id`),
  CONSTRAINT `fk_personal_id` FOREIGN KEY (`personal_id`) REFERENCES `personal_humanitario` (`cedula`),
  CONSTRAINT `fk_ruta_id` FOREIGN KEY (`ruta_id`) REFERENCES `rutas` (`id_ruta`),
  CONSTRAINT `fk_vehiculo_id` FOREIGN KEY (`vehiculo_id`) REFERENCES `vehiculos` (`id_vehiculo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `asignacion_logistica`
--

LOCK TABLES `asignacion_logistica` WRITE;
/*!40000 ALTER TABLE `asignacion_logistica` DISABLE KEYS */;
/*!40000 ALTER TABLE `asignacion_logistica` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `asignacion_tareas`
--

DROP TABLE IF EXISTS `asignacion_tareas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `asignacion_tareas` (
  `id_asignacion` int NOT NULL,
  `personal_id` int NOT NULL,
  `tarea` varchar(200) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL,
  `ubicacion_asignada` varchar(100) NOT NULL,
  `estado` varchar(100) NOT NULL,
  PRIMARY KEY (`id_asignacion`),
  UNIQUE KEY `id_asignacion_UNIQUE` (`id_asignacion`),
  UNIQUE KEY `personal_id_UNIQUE` (`personal_id`),
  KEY `personal_id_idx` (`personal_id`),
  CONSTRAINT `personal_id` FOREIGN KEY (`personal_id`) REFERENCES `personal_humanitario` (`cedula`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `asignacion_tareas`
--

LOCK TABLES `asignacion_tareas` WRITE;
/*!40000 ALTER TABLE `asignacion_tareas` DISABLE KEYS */;
/*!40000 ALTER TABLE `asignacion_tareas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `beneficiarios`
--

DROP TABLE IF EXISTS `beneficiarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `beneficiarios` (
  `Cedula` int NOT NULL,
  `primer_nombre` varchar(100) NOT NULL,
  `primer_apellido` varchar(100) NOT NULL,
  `segundo_apellido` varchar(100) DEFAULT NULL,
  `segundo_nombre` varchar(45) DEFAULT NULL,
  `fecha_nacimiento` date NOT NULL,
  `genero` varchar(10) DEFAULT NULL,
  `telefono` varchar(20) NOT NULL,
  `correo` varchar(100) NOT NULL,
  `direccion` text NOT NULL,
  `estado_id` int NOT NULL,
  `municipio_id` int NOT NULL,
  `fecha_registro` date DEFAULT NULL,
  `edad` int DEFAULT NULL,
  PRIMARY KEY (`Cedula`),
  UNIQUE KEY `Cedula_UNIQUE` (`Cedula`),
  KEY `beneficiarios_ibfk_1` (`estado_id`),
  KEY `beneficiarios_ibfk_2` (`municipio_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `beneficiarios`
--

LOCK TABLES `beneficiarios` WRITE;
/*!40000 ALTER TABLE `beneficiarios` DISABLE KEYS */;
INSERT INTO `beneficiarios` VALUES (1,'Carlitos','Johnson','Las Flores','Bartolomeo','1967-08-11','M','32546879','Cj@hotmail.com','San fierro',1,18,'2025-05-19',19),(2,'Juan','Pérez','Ramírez','Carlos','1990-05-14','Masculino','555-1234','juan.perez@example.com','Calle 123, Colonia Centro',1,10,'2025-05-20',35),(3,'María','López','García','Fernanda','1988-08-22','Femenino','555-5678','maria.lopez@example.com','Avenida Siempre Viva 742',2,15,'2025-05-20',36),(4,'Carlos','Martínez','Rojas','Andrés','1995-11-10','Masculino','555-9012','carlos.martinez@example.com','Calle Reforma 101',3,20,'2025-05-20',29),(5,'Ana','González','Mendoza','Lucía','2000-01-05','Femenino','555-3456','ana.gonzalez@example.com','Boulevard del Sol #45',4,25,'2025-05-20',25),(6,'Luis','Sánchez','Torres','Miguel','1985-03-18','Masculino','555-7890','luis.sanchez@example.com','Privada del Lago #12',1,12,'2025-05-20',40),(7,'Sofía','Ramírez','Delgado','Isabel','1992-06-30','Femenino','555-2345','sofia.ramirez@example.com','Colonia Jardines, Manzana 8',2,18,'2025-05-20',32),(8,'Pedro','Castillo','Aguilar','José','1998-09-12','Masculino','555-6789','pedro.castillo@example.com','Callejón del Norte #7',3,19,'2025-05-20',26),(9,'Laura','Hernández','Vega','Beatriz','1987-12-01','Femenino','555-1122','laura.hernandez@example.com','Av. Universidad 500',5,8,'2025-05-20',37),(10,'Diego','Morales','Navarro','Alonso','1993-07-19','Masculino','555-3344','diego.morales@example.com','Calle Estrella del Mar 32',6,22,'2025-05-20',31),(11,'Camila','Ortiz','Campos','Josefina','2001-02-28','Femenino','555-5566','camila.ortiz@example.com','Zona Rural, Sector B',2,9,'2025-05-20',24);
/*!40000 ALTER TABLE `beneficiarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `beneficiarios_grupos`
--

DROP TABLE IF EXISTS `beneficiarios_grupos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `beneficiarios_grupos` (
  `Cedula` int NOT NULL,
  `grupo_id` int NOT NULL,
  KEY `grupo_id` (`grupo_id`),
  KEY `beneficiarios_grupos_cedula_idx` (`Cedula`),
  CONSTRAINT `beneficiarios_grupos_cedula` FOREIGN KEY (`Cedula`) REFERENCES `beneficiarios` (`Cedula`),
  CONSTRAINT `beneficiarios_grupos_ibfk_2` FOREIGN KEY (`grupo_id`) REFERENCES `grupos_vulnerables` (`id_grupo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `beneficiarios_grupos`
--

LOCK TABLES `beneficiarios_grupos` WRITE;
/*!40000 ALTER TABLE `beneficiarios_grupos` DISABLE KEYS */;
/*!40000 ALTER TABLE `beneficiarios_grupos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `beneficiarios_programas`
--

DROP TABLE IF EXISTS `beneficiarios_programas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `beneficiarios_programas` (
  `Cedula` int NOT NULL,
  `programa_id` int NOT NULL,
  `fecha_asignacion` date NOT NULL,
  `estatus` varchar(50) DEFAULT NULL,
  KEY `programa_id` (`programa_id`),
  KEY `fecha_asignacion_idx` (`fecha_asignacion`),
  KEY `Cedula_programas_idx` (`Cedula`),
  CONSTRAINT `beneficiarios_programas_ibfk_2` FOREIGN KEY (`programa_id`) REFERENCES `programas` (`id_programa`),
  CONSTRAINT `Cedula_programas` FOREIGN KEY (`Cedula`) REFERENCES `beneficiarios` (`Cedula`),
  CONSTRAINT `fecha_asignacion` FOREIGN KEY (`fecha_asignacion`) REFERENCES `fecha_donacion` (`donacion_fecha`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `beneficiarios_programas`
--

LOCK TABLES `beneficiarios_programas` WRITE;
/*!40000 ALTER TABLE `beneficiarios_programas` DISABLE KEYS */;
/*!40000 ALTER TABLE `beneficiarios_programas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `capacitaciones`
--

DROP TABLE IF EXISTS `capacitaciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `capacitaciones` (
  `id_capacitacion` int NOT NULL,
  `personal_id` int NOT NULL,
  `nombre_capacitacion` varchar(150) NOT NULL,
  `fecha_capacitacion` date NOT NULL,
  `institucion` varchar(100) NOT NULL,
  `estado_capacitacion` varchar(45) NOT NULL,
  PRIMARY KEY (`id_capacitacion`),
  UNIQUE KEY `id_capacitacion_UNIQUE` (`id_capacitacion`),
  UNIQUE KEY `personal_id_UNIQUE` (`personal_id`),
  CONSTRAINT `personal_id_capacitaciones` FOREIGN KEY (`personal_id`) REFERENCES `personal_humanitario` (`cedula`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `capacitaciones`
--

LOCK TABLES `capacitaciones` WRITE;
/*!40000 ALTER TABLE `capacitaciones` DISABLE KEYS */;
/*!40000 ALTER TABLE `capacitaciones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categorias_inventario`
--

DROP TABLE IF EXISTS `categorias_inventario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categorias_inventario` (
  `id_categoria` int NOT NULL,
  `nombre_categoria` varchar(100) NOT NULL,
  PRIMARY KEY (`id_categoria`),
  UNIQUE KEY `id_categoria_UNIQUE` (`id_categoria`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categorias_inventario`
--

LOCK TABLES `categorias_inventario` WRITE;
/*!40000 ALTER TABLE `categorias_inventario` DISABLE KEYS */;
/*!40000 ALTER TABLE `categorias_inventario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comunicacion_donantes`
--

DROP TABLE IF EXISTS `comunicacion_donantes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comunicacion_donantes` (
  `id_comunicacion` int NOT NULL,
  `id_donante` int NOT NULL,
  `mensaje` int NOT NULL,
  `contacto` int NOT NULL,
  PRIMARY KEY (`id_comunicacion`),
  UNIQUE KEY `id_comunicacion_UNIQUE` (`id_comunicacion`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comunicacion_donantes`
--

LOCK TABLES `comunicacion_donantes` WRITE;
/*!40000 ALTER TABLE `comunicacion_donantes` DISABLE KEYS */;
/*!40000 ALTER TABLE `comunicacion_donantes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `conductor`
--

DROP TABLE IF EXISTS `conductor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `conductor` (
  `id_conductor` int NOT NULL,
  `vehiculo_id` int NOT NULL,
  `ruta_id` int NOT NULL,
  `edad` int NOT NULL,
  `nombre` varchar(45) NOT NULL,
  `apellido` varchar(45) NOT NULL,
  `licencia` varchar(45) NOT NULL,
  `telefono` varchar(50) NOT NULL,
  PRIMARY KEY (`id_conductor`),
  UNIQUE KEY `id_conductor_UNIQUE` (`id_conductor`),
  UNIQUE KEY `ruta_id_UNIQUE` (`ruta_id`),
  UNIQUE KEY `licencia_UNIQUE` (`licencia`),
  KEY `vehiculo_id_conductor_idx` (`vehiculo_id`),
  KEY `ruta_id_conductor_idx` (`ruta_id`),
  CONSTRAINT `ruta_id_conductor` FOREIGN KEY (`ruta_id`) REFERENCES `rutas` (`id_ruta`),
  CONSTRAINT `vehiculo_id_conductor` FOREIGN KEY (`vehiculo_id`) REFERENCES `vehiculos` (`id_vehiculo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `conductor`
--

LOCK TABLES `conductor` WRITE;
/*!40000 ALTER TABLE `conductor` DISABLE KEYS */;
/*!40000 ALTER TABLE `conductor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `coordinadores`
--

DROP TABLE IF EXISTS `coordinadores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `coordinadores` (
  `id_coordinadores` int NOT NULL,
  `nombre` varchar(45) NOT NULL,
  `apellido` varchar(45) NOT NULL,
  `coordinadorescol` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id_coordinadores`),
  UNIQUE KEY `id_coordinadores_UNIQUE` (`id_coordinadores`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `coordinadores`
--

LOCK TABLES `coordinadores` WRITE;
/*!40000 ALTER TABLE `coordinadores` DISABLE KEYS */;
/*!40000 ALTER TABLE `coordinadores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `distribucion_logistica`
--

DROP TABLE IF EXISTS `distribucion_logistica`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `distribucion_logistica` (
  `id_distribucion` int NOT NULL,
  `almacen_id` int NOT NULL,
  `logistica_id` int NOT NULL,
  `producto_id` int NOT NULL,
  `ruta_id` int NOT NULL,
  `cantidad` int NOT NULL,
  `fecha_entrega` date NOT NULL,
  PRIMARY KEY (`id_distribucion`),
  UNIQUE KEY `logistica_id_UNIQUE` (`logistica_id`),
  UNIQUE KEY `almacen_id_UNIQUE` (`almacen_id`),
  UNIQUE KEY `id_distribucion_UNIQUE` (`id_distribucion`),
  UNIQUE KEY `ruta_id_UNIQUE` (`ruta_id`),
  KEY `fk_almacen_id_idx` (`almacen_id`),
  KEY `fk_producto_id_idx` (`producto_id`),
  KEY `fk_ruta_id_idx` (`ruta_id`),
  KEY `ruta_id_idx` (`ruta_id`),
  KEY `logistica_id_idx` (`logistica_id`),
  CONSTRAINT `fk_almacen_id` FOREIGN KEY (`almacen_id`) REFERENCES `almacen` (`id_almacen`),
  CONSTRAINT `fk_producto_id` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id_producto`),
  CONSTRAINT `logistica_id_distribucion` FOREIGN KEY (`logistica_id`) REFERENCES `logistica` (`id_logistica`),
  CONSTRAINT `ruta_id` FOREIGN KEY (`ruta_id`) REFERENCES `rutas` (`id_ruta`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `distribucion_logistica`
--

LOCK TABLES `distribucion_logistica` WRITE;
/*!40000 ALTER TABLE `distribucion_logistica` DISABLE KEYS */;
/*!40000 ALTER TABLE `distribucion_logistica` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `distribucion_productos`
--

DROP TABLE IF EXISTS `distribucion_productos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `distribucion_productos` (
  `id_distribucion` int NOT NULL,
  `producto_id` int NOT NULL,
  `cedula_beneficiario` int NOT NULL,
  `cedula_personal` int NOT NULL,
  `fecha_distribucion` date NOT NULL,
  `cantidad` int NOT NULL,
  `almacen_id` int NOT NULL,
  `ruta_id` int NOT NULL,
  PRIMARY KEY (`id_distribucion`),
  UNIQUE KEY `id_distribucion_UNIQUE` (`id_distribucion`),
  UNIQUE KEY `almacen_id_UNIQUE` (`almacen_id`),
  UNIQUE KEY `cedula_beneficiario_UNIQUE` (`cedula_beneficiario`),
  KEY `producto_id_idx` (`producto_id`),
  KEY `beneficiario_id_idx` (`cedula_beneficiario`),
  KEY `almacen_id_idx` (`almacen_id`),
  KEY `ruta_id_idx` (`ruta_id`),
  KEY `cedula_personal_productos_idx` (`cedula_personal`),
  CONSTRAINT `almacen_id` FOREIGN KEY (`almacen_id`) REFERENCES `almacen` (`id_almacen`),
  CONSTRAINT `cedula_beneficiarios_distribucion` FOREIGN KEY (`cedula_beneficiario`) REFERENCES `beneficiarios` (`Cedula`),
  CONSTRAINT `cedula_personal_productos` FOREIGN KEY (`cedula_personal`) REFERENCES `personal_humanitario` (`cedula`),
  CONSTRAINT `producto_id` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id_producto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `distribucion_productos`
--

LOCK TABLES `distribucion_productos` WRITE;
/*!40000 ALTER TABLE `distribucion_productos` DISABLE KEYS */;
/*!40000 ALTER TABLE `distribucion_productos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `documentos_beneficiarios`
--

DROP TABLE IF EXISTS `documentos_beneficiarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `documentos_beneficiarios` (
  `id_documento` int NOT NULL,
  `cedula_beneficiario` int NOT NULL,
  `nombre_documento` varchar(255) NOT NULL,
  `ruta_archivo` varchar(500) NOT NULL,
  `fecha_subida` date NOT NULL,
  PRIMARY KEY (`id_documento`),
  UNIQUE KEY `id_documento_UNIQUE` (`id_documento`),
  KEY `documentos_beneficiarios_ibfk_1_idx` (`cedula_beneficiario`),
  CONSTRAINT `documentos_beneficiarios_ibfk_1` FOREIGN KEY (`cedula_beneficiario`) REFERENCES `beneficiarios` (`Cedula`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `documentos_beneficiarios`
--

LOCK TABLES `documentos_beneficiarios` WRITE;
/*!40000 ALTER TABLE `documentos_beneficiarios` DISABLE KEYS */;
/*!40000 ALTER TABLE `documentos_beneficiarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `donaciones`
--

DROP TABLE IF EXISTS `donaciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `donaciones` (
  `id_donacion` int NOT NULL AUTO_INCREMENT,
  `beneficiario_id` int NOT NULL,
  `donante_id` int NOT NULL,
  `fecha_donacion` date NOT NULL,
  `tipo_donacion` varchar(45) NOT NULL,
  `descripcion` text NOT NULL,
  `monto` decimal(10,2) NOT NULL,
  `categoria` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_donacion`),
  UNIQUE KEY `donante_id_UNIQUE` (`donante_id`),
  UNIQUE KEY `beneficiario_id_UNIQUE` (`beneficiario_id`),
  UNIQUE KEY `id_donacion_UNIQUE` (`id_donacion`),
  KEY `categoria_idx` (`categoria`),
  KEY `fk_fecha_donacion_idx` (`fecha_donacion`),
  KEY `beneficiario_idx` (`beneficiario_id`),
  KEY `fk_donante_id_donaciones_idx` (`donante_id`),
  CONSTRAINT `cedula_beneficiario` FOREIGN KEY (`beneficiario_id`) REFERENCES `beneficiarios` (`Cedula`),
  CONSTRAINT `cedula_donante` FOREIGN KEY (`donante_id`) REFERENCES `donantes` (`Cedula_Donante`),
  CONSTRAINT `fecha_donaciones` FOREIGN KEY (`fecha_donacion`) REFERENCES `fecha_donacion` (`donacion_fecha`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `donaciones`
--

LOCK TABLES `donaciones` WRITE;
/*!40000 ALTER TABLE `donaciones` DISABLE KEYS */;
/*!40000 ALTER TABLE `donaciones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `donantes`
--

DROP TABLE IF EXISTS `donantes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `donantes` (
  `Cedula_Donante` int NOT NULL,
  `contacto` varchar(150) NOT NULL,
  `primer_nombre` varchar(100) NOT NULL,
  `segundo_nombre` varchar(45) NOT NULL,
  `primer_apeliido` varchar(45) NOT NULL,
  `segundo_apellido` varchar(45) NOT NULL,
  `clave` varchar(100) NOT NULL,
  PRIMARY KEY (`Cedula_Donante`),
  UNIQUE KEY `Cedula_Donantes_UNIQUE` (`Cedula_Donante`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `donantes`
--

LOCK TABLES `donantes` WRITE;
/*!40000 ALTER TABLE `donantes` DISABLE KEYS */;
INSERT INTO `donantes` VALUES (246810,'pedro@pereez.com','pedro','perez','gomez','gonzalez','12345'),(1070593043,'asdas@gmail.com','sadasd','asdasda','asdasd','asdasd','1234'),(1070593044,'kevin1018pro@gmail.com','Kevin','Santiago','Gonzalez','Bernate','1234'),(1070593045,'kevin1018pro@gmail.co','fdsfsdf','sdfsdf','sdfsdf','sdfsdf','1234');
/*!40000 ALTER TABLE `donantes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estados`
--

DROP TABLE IF EXISTS `estados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estados` (
  `id_estado` int NOT NULL,
  `nombre_estado` varchar(100) NOT NULL,
  PRIMARY KEY (`id_estado`),
  UNIQUE KEY `id_estado_UNIQUE` (`id_estado`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estados`
--

LOCK TABLES `estados` WRITE;
/*!40000 ALTER TABLE `estados` DISABLE KEYS */;
/*!40000 ALTER TABLE `estados` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fecha_donacion`
--

DROP TABLE IF EXISTS `fecha_donacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fecha_donacion` (
  `donacion_fecha` date NOT NULL,
  PRIMARY KEY (`donacion_fecha`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fecha_donacion`
--

LOCK TABLES `fecha_donacion` WRITE;
/*!40000 ALTER TABLE `fecha_donacion` DISABLE KEYS */;
INSERT INTO `fecha_donacion` VALUES ('2025-05-19'),('2025-05-20');
/*!40000 ALTER TABLE `fecha_donacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gestor_donaciones`
--

DROP TABLE IF EXISTS `gestor_donaciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gestor_donaciones` (
  `radicacion` enum('Radicado','Asignado','Finalizado') NOT NULL,
  `informes_id` int NOT NULL,
  `seguimiento_id` int NOT NULL,
  `fecha` date NOT NULL,
  `gestor_donacionescol` varchar(45) DEFAULT NULL,
  UNIQUE KEY `informes_id_UNIQUE` (`informes_id`),
  UNIQUE KEY `seguimiento_id_UNIQUE` (`seguimiento_id`),
  KEY `fk_informe_id_idx` (`informes_id`),
  KEY `fecha_idx` (`fecha`),
  CONSTRAINT `informes_id` FOREIGN KEY (`informes_id`) REFERENCES `informes` (`id_informe`),
  CONSTRAINT `seguimiento_id` FOREIGN KEY (`seguimiento_id`) REFERENCES `seguimiento_donante` (`id_seguimiento`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gestor_donaciones`
--

LOCK TABLES `gestor_donaciones` WRITE;
/*!40000 ALTER TABLE `gestor_donaciones` DISABLE KEYS */;
/*!40000 ALTER TABLE `gestor_donaciones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `grupos_vulnerables`
--

DROP TABLE IF EXISTS `grupos_vulnerables`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `grupos_vulnerables` (
  `id_grupo` int NOT NULL,
  `nombre_grupo` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_grupo`),
  UNIQUE KEY `id_grupo_UNIQUE` (`id_grupo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grupos_vulnerables`
--

LOCK TABLES `grupos_vulnerables` WRITE;
/*!40000 ALTER TABLE `grupos_vulnerables` DISABLE KEYS */;
INSERT INTO `grupos_vulnerables` VALUES (5001,'zeus');
/*!40000 ALTER TABLE `grupos_vulnerables` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `historial_beneficiarios`
--

DROP TABLE IF EXISTS `historial_beneficiarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `historial_beneficiarios` (
  `id_historial` int NOT NULL,
  `cedula` int NOT NULL,
  `fecha_donacion` date NOT NULL,
  `detalle_cambio` text,
  `usuario_modifico` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_historial`),
  UNIQUE KEY `id_historial_UNIQUE` (`id_historial`),
  UNIQUE KEY `cedula_UNIQUE` (`cedula`),
  KEY `Cedula_historial_idx` (`cedula`),
  CONSTRAINT `Cedula_historial` FOREIGN KEY (`cedula`) REFERENCES `beneficiarios` (`Cedula`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historial_beneficiarios`
--

LOCK TABLES `historial_beneficiarios` WRITE;
/*!40000 ALTER TABLE `historial_beneficiarios` DISABLE KEYS */;
/*!40000 ALTER TABLE `historial_beneficiarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `informes`
--

DROP TABLE IF EXISTS `informes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `informes` (
  `id_informe` int NOT NULL,
  `cedula_donante` int NOT NULL,
  `cedula_beneficiario` int NOT NULL,
  `estado_id` int NOT NULL,
  `historial_id` int NOT NULL,
  `donacion_id` int NOT NULL,
  `seguimiento_id` int NOT NULL,
  `cedula_personal` int NOT NULL,
  `fecha_donacion` date NOT NULL,
  PRIMARY KEY (`id_informe`),
  UNIQUE KEY `id_informe_UNIQUE` (`id_informe`),
  UNIQUE KEY `donacion_id_UNIQUE` (`donacion_id`),
  UNIQUE KEY `seguimiento_id_UNIQUE` (`seguimiento_id`),
  UNIQUE KEY `historial_id_UNIQUE` (`historial_id`),
  UNIQUE KEY `cedula_beneficiario_UNIQUE` (`cedula_beneficiario`),
  KEY `donantes_id_idx` (`cedula_donante`),
  KEY `estados_id_idx` (`estado_id`),
  KEY `donacion_id_idx` (`donacion_id`),
  KEY `personal_id_idx` (`cedula_personal`),
  KEY `fecha_donacion_idx` (`fecha_donacion`),
  KEY `historial_id_idx` (`historial_id`),
  KEY `cedula_beneficiarios_idx` (`cedula_beneficiario`),
  CONSTRAINT `cedula_beneficiarios` FOREIGN KEY (`cedula_beneficiario`) REFERENCES `beneficiarios` (`Cedula`),
  CONSTRAINT `donacion_id_informes` FOREIGN KEY (`donacion_id`) REFERENCES `donaciones` (`id_donacion`),
  CONSTRAINT `donantes_id` FOREIGN KEY (`cedula_donante`) REFERENCES `donantes` (`Cedula_Donante`),
  CONSTRAINT `estados_id` FOREIGN KEY (`estado_id`) REFERENCES `estados` (`id_estado`),
  CONSTRAINT `fecha_donacion` FOREIGN KEY (`fecha_donacion`) REFERENCES `fecha_donacion` (`donacion_fecha`),
  CONSTRAINT `historial_id` FOREIGN KEY (`historial_id`) REFERENCES `historial_beneficiarios` (`id_historial`),
  CONSTRAINT `personal_id_informe` FOREIGN KEY (`cedula_personal`) REFERENCES `personal_humanitario` (`cedula`),
  CONSTRAINT `seguimiento_id_donante` FOREIGN KEY (`seguimiento_id`) REFERENCES `seguimiento_donante` (`id_seguimiento`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `informes`
--

LOCK TABLES `informes` WRITE;
/*!40000 ALTER TABLE `informes` DISABLE KEYS */;
/*!40000 ALTER TABLE `informes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ingreso_productos`
--

DROP TABLE IF EXISTS `ingreso_productos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ingreso_productos` (
  `id_ingreso` int NOT NULL,
  `donacion_id` int NOT NULL,
  `producto_id` int NOT NULL,
  `cantidad_ingresada` int NOT NULL,
  `fecha_ingreso` date NOT NULL,
  PRIMARY KEY (`id_ingreso`),
  UNIQUE KEY `id_ingreso_UNIQUE` (`id_ingreso`),
  UNIQUE KEY `donacion_id_UNIQUE` (`donacion_id`),
  UNIQUE KEY `producto_id_UNIQUE` (`producto_id`),
  KEY `fk_producto_id_ingreso_idx` (`producto_id`),
  KEY `donacion_id_idx` (`donacion_id`),
  CONSTRAINT `donacion_id` FOREIGN KEY (`donacion_id`) REFERENCES `donaciones` (`id_donacion`),
  CONSTRAINT `fk_producto_id_ingreso` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id_producto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ingreso_productos`
--

LOCK TABLES `ingreso_productos` WRITE;
/*!40000 ALTER TABLE `ingreso_productos` DISABLE KEYS */;
/*!40000 ALTER TABLE `ingreso_productos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `logistica`
--

DROP TABLE IF EXISTS `logistica`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `logistica` (
  `id_logistica` int NOT NULL,
  `ubicacion_id` varchar(45) NOT NULL,
  `locacion_id` varchar(45) NOT NULL,
  PRIMARY KEY (`id_logistica`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logistica`
--

LOCK TABLES `logistica` WRITE;
/*!40000 ALTER TABLE `logistica` DISABLE KEYS */;
/*!40000 ALTER TABLE `logistica` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lote`
--

DROP TABLE IF EXISTS `lote`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lote` (
  `id_lote` int NOT NULL,
  `nombre_lote` varchar(100) NOT NULL,
  `fecha_vencimiento` date NOT NULL,
  `compania` varchar(200) NOT NULL,
  `cantidad` int NOT NULL,
  PRIMARY KEY (`id_lote`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lote`
--

LOCK TABLES `lote` WRITE;
/*!40000 ALTER TABLE `lote` DISABLE KEYS */;
/*!40000 ALTER TABLE `lote` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `municipios`
--

DROP TABLE IF EXISTS `municipios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `municipios` (
  `id_municipio` int NOT NULL,
  `nombre_municipio` varchar(100) NOT NULL,
  `estado_id` int NOT NULL,
  PRIMARY KEY (`id_municipio`),
  UNIQUE KEY `id_municipio_UNIQUE` (`id_municipio`),
  KEY `estado_id` (`estado_id`),
  CONSTRAINT `municipios_ibfk_1` FOREIGN KEY (`estado_id`) REFERENCES `estados` (`id_estado`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `municipios`
--

LOCK TABLES `municipios` WRITE;
/*!40000 ALTER TABLE `municipios` DISABLE KEYS */;
/*!40000 ALTER TABLE `municipios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `necesidades_beneficiarios`
--

DROP TABLE IF EXISTS `necesidades_beneficiarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `necesidades_beneficiarios` (
  `id_necesidad` int NOT NULL,
  `Cedula` int NOT NULL,
  `tipo_necesidad` varchar(100) DEFAULT NULL,
  `descripcion` text,
  `nivel_urgencia` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_necesidad`),
  UNIQUE KEY `id_necesidad_UNIQUE` (`id_necesidad`),
  KEY `necesidades_beneficiarios_ibfk_1_idx` (`Cedula`),
  CONSTRAINT `necesidades_beneficiarios_ibfk_1` FOREIGN KEY (`Cedula`) REFERENCES `beneficiarios` (`Cedula`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `necesidades_beneficiarios`
--

LOCK TABLES `necesidades_beneficiarios` WRITE;
/*!40000 ALTER TABLE `necesidades_beneficiarios` DISABLE KEYS */;
/*!40000 ALTER TABLE `necesidades_beneficiarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nivel_necesidad_beneficiarios`
--

DROP TABLE IF EXISTS `nivel_necesidad_beneficiarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nivel_necesidad_beneficiarios` (
  `id_nivel` int NOT NULL,
  `cedula` int NOT NULL,
  `nivel` int DEFAULT NULL,
  `comentarios` text,
  PRIMARY KEY (`id_nivel`),
  UNIQUE KEY `id_nivel_UNIQUE` (`id_nivel`),
  KEY `beneficiario_id` (`cedula`),
  CONSTRAINT `nivel_necesidad_beneficiarios_ibfk_1` FOREIGN KEY (`cedula`) REFERENCES `beneficiarios` (`Cedula`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nivel_necesidad_beneficiarios`
--

LOCK TABLES `nivel_necesidad_beneficiarios` WRITE;
/*!40000 ALTER TABLE `nivel_necesidad_beneficiarios` DISABLE KEYS */;
/*!40000 ALTER TABLE `nivel_necesidad_beneficiarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `personal_humanitario`
--

DROP TABLE IF EXISTS `personal_humanitario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `personal_humanitario` (
  `cedula` int NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `edad` int NOT NULL,
  `genero` varchar(45) NOT NULL,
  `ubicacion` varchar(100) NOT NULL,
  `profesion` varchar(100) NOT NULL,
  `habilidades` text NOT NULL,
  `especializaciones` text NOT NULL,
  `disponibilidad` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`cedula`),
  UNIQUE KEY `cedula_UNIQUE` (`cedula`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `personal_humanitario`
--

LOCK TABLES `personal_humanitario` WRITE;
/*!40000 ALTER TABLE `personal_humanitario` DISABLE KEYS */;
/*!40000 ALTER TABLE `personal_humanitario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productos`
--

DROP TABLE IF EXISTS `productos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `productos` (
  `id_producto` int NOT NULL,
  `categoria_id` int NOT NULL,
  `tipo_producto` enum('Comida','Medicina') NOT NULL,
  `stock_minimo` int NOT NULL,
  `lote_id` int NOT NULL,
  `descripcion` text,
  PRIMARY KEY (`id_producto`),
  UNIQUE KEY `lote_id_UNIQUE` (`lote_id`),
  UNIQUE KEY `categoria_id_UNIQUE` (`categoria_id`),
  UNIQUE KEY `id_producto_UNIQUE` (`id_producto`),
  KEY `lote_id_idx` (`lote_id`),
  KEY `categoria_id_idx` (`categoria_id`),
  CONSTRAINT `categoria_id` FOREIGN KEY (`categoria_id`) REFERENCES `categorias_inventario` (`id_categoria`),
  CONSTRAINT `lote_id` FOREIGN KEY (`lote_id`) REFERENCES `lote` (`id_lote`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos`
--

LOCK TABLES `productos` WRITE;
/*!40000 ALTER TABLE `productos` DISABLE KEYS */;
/*!40000 ALTER TABLE `productos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `programas`
--

DROP TABLE IF EXISTS `programas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `programas` (
  `id_programa` int NOT NULL,
  `nombre_programa` varchar(100) NOT NULL,
  `descripcion` text,
  `fecha_inicio` date DEFAULT NULL,
  `fecha_fin` date DEFAULT NULL,
  PRIMARY KEY (`id_programa`),
  UNIQUE KEY `id_programa_UNIQUE` (`id_programa`),
  UNIQUE KEY `nombre_programa_UNIQUE` (`nombre_programa`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `programas`
--

LOCK TABLES `programas` WRITE;
/*!40000 ALTER TABLE `programas` DISABLE KEYS */;
/*!40000 ALTER TABLE `programas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rutas`
--

DROP TABLE IF EXISTS `rutas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rutas` (
  `id_ruta` int NOT NULL,
  `origen` varchar(100) NOT NULL,
  `destino` varchar(100) NOT NULL,
  `condiciones_seg` longtext NOT NULL,
  `fecha_planificada` date NOT NULL,
  PRIMARY KEY (`id_ruta`),
  UNIQUE KEY `id_ruta_UNIQUE` (`id_ruta`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rutas`
--

LOCK TABLES `rutas` WRITE;
/*!40000 ALTER TABLE `rutas` DISABLE KEYS */;
/*!40000 ALTER TABLE `rutas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `seguimiento_beneficiario`
--

DROP TABLE IF EXISTS `seguimiento_beneficiario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `seguimiento_beneficiario` (
  `id_seguimiento` int NOT NULL,
  `cedula_beneficiario` int NOT NULL,
  `cedula_personal` int NOT NULL,
  `fecha` date NOT NULL,
  `observaciones` text NOT NULL,
  PRIMARY KEY (`id_seguimiento`),
  UNIQUE KEY `id_seguimiento_UNIQUE` (`id_seguimiento`) /*!80000 INVISIBLE */,
  UNIQUE KEY `cedula_beneficiario_UNIQUE` (`cedula_beneficiario`),
  KEY `cedula_personal_seguimiento_idx` (`cedula_personal`),
  CONSTRAINT `cedula_beneficiario_seguimiento` FOREIGN KEY (`cedula_beneficiario`) REFERENCES `beneficiarios` (`Cedula`),
  CONSTRAINT `cedula_personal_seguimiento` FOREIGN KEY (`cedula_personal`) REFERENCES `personal_humanitario` (`cedula`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `seguimiento_beneficiario`
--

LOCK TABLES `seguimiento_beneficiario` WRITE;
/*!40000 ALTER TABLE `seguimiento_beneficiario` DISABLE KEYS */;
/*!40000 ALTER TABLE `seguimiento_beneficiario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `seguimiento_donante`
--

DROP TABLE IF EXISTS `seguimiento_donante`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `seguimiento_donante` (
  `id_seguimiento` int NOT NULL,
  `donaciones_id` int NOT NULL,
  `fecha` date NOT NULL,
  `ingreso` int NOT NULL,
  `egreso` int NOT NULL,
  PRIMARY KEY (`id_seguimiento`),
  UNIQUE KEY `id_seguimiento_UNIQUE` (`id_seguimiento`),
  KEY `fecha_idx` (`fecha`),
  KEY `ingreso_seguimiento_idx` (`ingreso`),
  KEY `donaciones_id_seguimiento_idx` (`donaciones_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `seguimiento_donante`
--

LOCK TABLES `seguimiento_donante` WRITE;
/*!40000 ALTER TABLE `seguimiento_donante` DISABLE KEYS */;
INSERT INTO `seguimiento_donante` VALUES (1,15,'2025-05-20',1,0),(2,16,'2025-05-20',1,0),(3,17,'2025-05-20',1,0);
/*!40000 ALTER TABLE `seguimiento_donante` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vehiculos`
--

DROP TABLE IF EXISTS `vehiculos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vehiculos` (
  `id_vehiculo` int NOT NULL,
  `placa` varchar(20) NOT NULL,
  `tipo` varchar(50) NOT NULL,
  `estado` varchar(50) NOT NULL,
  `fecha_mantenimiento` date NOT NULL,
  PRIMARY KEY (`id_vehiculo`),
  UNIQUE KEY `id_vehiculo_UNIQUE` (`id_vehiculo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vehiculos`
--

LOCK TABLES `vehiculos` WRITE;
/*!40000 ALTER TABLE `vehiculos` DISABLE KEYS */;
/*!40000 ALTER TABLE `vehiculos` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-27 20:53:10
