CREATE DATABASE bbdd_tareas;

\c bbdd_tareas;

CREATE TABLE usuarios (usuario VARCHAR(20) PRIMARY KEY,
						nombre VARCHAR(20),
						apellido1 VARCHAR(20),
						apellido2 VARCHAR(20),
						contrasena VARCHAR(70),
						edad INT,
						ciudad VARCHAR(20),
						pais VARCHAR(20));
