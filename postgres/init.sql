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

CREATE TABLE tareas (id_tarea VARCHAR(32) PRIMARY KEY,
					usuario VARCHAR(20),
					titulo VARCHAR(20),
					descripcion VARCHAR(300),
					categoria VARCHAR(20),
					completada BOOL DEFAULT False,
					comentario VARCHAR(300) DEFAULT NULL,
					fecha_creacion DATE,
					fecha_completada DATE DEFAULT NULL,
					FOREIGN KEY (usuario) REFERENCES usuarios(usuario) ON DELETE CASCADE);
