import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Dict, List, Optional

from .confconexion import *

# Clase para la conexion a la BBDD
class Conexion:

	def __init__(self)->None:

		try:
			
			self.bbdd=psycopg2.connect(host=HOST, user=USUARIO, password=CONTRASENA, port=PUERTO, database=BBDD)
			self.c=self.bbdd.cursor(cursor_factory=RealDictCursor)

		except psycopg2.OperationalError as e:

			print("Error en la conexion a la BBDD")
			print(e)

	# Metodo para cerrar la conexion a la BBDD
	def cerrarConexion(self)->None:

		self.c.close()
		self.bbdd.close()

	# Metodo para insertar un usuario
	def insertarUsuario(self, usuario:str, nombre:str, apellido1:str, apellido2:str, contrasena:str, edad:int, ciudad:str, pais:str)->None:

		self.c.execute("""INSERT INTO usuarios
						VALUES(%s, %s, %s, %s, %s, %s, %s, %s)""",
						(usuario, nombre, apellido1, apellido2, contrasena, edad, ciudad, pais))

		self.bbdd.commit()

	# Metodo para comprobar que un usuario existe
	def existe_usuario(self, usuario:str)->bool:

		self.c.execute("""SELECT *
						FROM usuarios
						WHERE usuario=%s""",
						(usuario,))

		return False if (self.c.fetchone() is None) else True


	# Metodo para obtener los usuarios
	def obtenerUsuarios(self)->Optional[List[Dict]]:

		self.c.execute("""SELECT nombre, apellido1
						FROM usuarios""")

		usuarios=self.c.fetchall()

		return None if usuarios==[] else usuarios

	# Metodo para obtener la contraseña (hash) del usuario
	def obtenerContrasena(self, usuario:str)->Optional[str]:

		self.c.execute("""SELECT contrasena
						FROM usuarios
						WHERE usuario=%s""",
						(usuario,))

		contrasena=self.c.fetchone()

		return contrasena["contrasena"] if contrasena is not None else contrasena

	# Metodo para obtener los datos de un usuario
	def obtenerDatosUsuario(self, usuario:str)->Optional[Dict]:

		self.c.execute("""SELECT usuario, nombre, apellido1, apellido2, edad, ciudad, pais
						FROM usuarios
						WHERE usuario=%s""",
						(usuario,))

		return self.c.fetchone()

	# Metodo para insertar una tarea
	def insertarTarea(self, id_tarea:str, usuario:str, titulo:str, descripcion:str, categoria:str, fecha_creacion:str)->None:

		self.c.execute("""INSERT INTO tareas (id_tarea, usuario, titulo, descripcion, categoria, fecha_creacion)
						VALUES(%s, %s, %s, %s, %s, %s)""",
						(id_tarea, usuario, titulo, descripcion, categoria, fecha_creacion))

		self.bbdd.commit()