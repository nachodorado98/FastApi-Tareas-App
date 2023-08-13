from fastapi import APIRouter, status, Depends
from typing import Dict
import datetime
import uuid

from src.database.sesion import crearConexion
from src.database.conexion import Conexion

from src.modelos.token import Payload
from src.modelos.tarea import TareaBBDD

from src.autenticacion.utils_auth import decodificarToken


router_tareas=APIRouter(prefix="/tareas", tags=["Tareas"])


@router_tareas.post("", status_code=status.HTTP_201_CREATED, summary="Crea una tarea")
async def crearTarea(tarea:TareaBBDD, payload:Payload=Depends(decodificarToken), con:Conexion=Depends(crearConexion))->Dict:

	"""
	Crea una tarea del usuario y la inserta en la BBDD.

	Devuelve un mensaje y el diccionario que representa a la tarea creada.

	## Respuesta

	201 (CREATED): Si se crea la tarea correctamente

	- **Mensaje**: El mensaje de creacion correcta de la tarea (str).
	- **Tarea**:  La tarea con su titulo y descripcion (Dict).

	401 (UNAUTHORIZED): Si los datos no son correctos

	- **Mensaje**: El mensaje de la excepcion (str).
	"""

	fecha_creacion=datetime.datetime.now().strftime("%Y-%m-%d")

	id_tarea=uuid.uuid4().hex

	con.insertarTarea(id_tarea, payload.sub, tarea.titulo, tarea.descripcion, tarea.categoria, fecha_creacion)

	con.cerrarConexion()

	return {"mensaje":"Tarea creada correctamente",
			"tarea":{"titulo":tarea.titulo, "descripcion":tarea.descripcion}}