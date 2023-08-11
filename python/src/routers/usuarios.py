from fastapi import APIRouter, status, Depends, HTTPException
from typing import List, Dict

from src.database.sesion import crearConexion
from src.database.conexion import Conexion

from src.modelos.usuario import Usuario, UsuarioBBDD, UsuarioBasico
from src.modelos.utils_usuario import obtenerObjetosUsuarioBasico

from src.utils import generarHash


router_usuarios=APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router_usuarios.post("", status_code=status.HTTP_201_CREATED, summary="Crea un usuario")
async def crearUsuario(usuario:UsuarioBBDD, con:Conexion=Depends(crearConexion))->Dict:

	"""
	Crea un usuario y lo inserta en la BBDD.

	Devuelve un mensaje y el diccionario que representa el usuario creado.

	## Respuesta

	201 (CREATED): Si se crea el usuario correctamente

	- **Mensaje**: El mensaje de creacion correcto del usuario (str).
	- **Usuario**: El usuario con el usuario y nombre (Dict).

	400 (BAD REQUEST): Si no se crea el usuario correctamente

	- **Mensaje**: El mensaje de la excepcion (str).
	"""

	if con.existe_usuario(usuario.usuario):

		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario existente")

	con.insertarUsuario(usuario.usuario,
						usuario.nombre,
						usuario.apellido1,
						usuario.apellido2,
						generarHash(usuario.contrasena),
						usuario.edad,
						usuario.ciudad,
						usuario.pais)

	con.cerrarConexion()

	return {"mensaje":"Usuario creado correctamente",
			"usuario":{"usuario":usuario.usuario, "nombre":usuario.nombre}}


@router_usuarios.get("", status_code=status.HTTP_200_OK, summary="Devuelve los usuarios existentes")
async def obtenerUsuarios(con:Conexion=Depends(crearConexion))->List[UsuarioBasico]:

	"""
	Devuelve los diccionarios asociados a los usuarios disponibles en la BBDD.

	## Respuesta

	200 (OK): Si se obtienen los usuarios correctamente

	- **Nombre**: El nombre del usuario (str).
	- **Apellido1**: El primer apellido del usuario (str).

	404 (NOT FOUND): Si no se obtienen los usuarios correctamente

	- **Mensaje**: El mensaje de la excepcion (str).
	"""

	usuarios=con.obtenerUsuarios()

	con.cerrarConexion()

	if usuarios is None:

		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuarios no existentes")

	return obtenerObjetosUsuarioBasico(usuarios)
	
