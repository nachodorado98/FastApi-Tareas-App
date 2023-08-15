from fastapi import APIRouter, status, Depends, HTTPException, Path
from typing import Dict, List
import datetime
import uuid

from src.database.sesion import crearConexion
from src.database.conexion import Conexion

from src.modelos.token import Payload
from src.modelos.tarea import TareaBBDD, Tarea
from src.modelos.utils_tarea import obtenerObjetosTarea, obtenerObjetoTarea

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


@router_tareas.get("", status_code=status.HTTP_200_OK, summary="Devuelve las tareas")
async def obtenerTareas(payload:Payload=Depends(decodificarToken), con:Conexion=Depends(crearConexion))->List[Tarea]:

	"""
	Devuelve los diccionarios asociados a las tareas disponibles en la BBDD del usuario.

	## Respuesta

	200 (OK): Si se obtienen las tareas correctamente

	- **Id_tarea**: El id de la tarea (str).
	- **Titulo**: El titulo de la tarea (str).
	- **Descripcion**: La descripcion de la tarea (str).
	- **Categoria**: La categoria de la tarea (str).
	- **Completada**: El estado de la tarea (bool).
	- **Comentario**: El comentario de la tarea (str).
	- **Fecha_creacion**: La fecha de creacion de la tarea (str).
	- **Fecha_completada**: La fecha de la realizacion de la tarea (str).

	401 (UNAUTHORIZED): Si los datos no son correctos

	- **Mensaje**: El mensaje de la excepcion (str).

	404 (NOT FOUND): Si no se obtienen las tareas correctamente

	- **Mensaje**: El mensaje de la excepcion (str).
	"""

	tareas=con.obtenerTareas(payload.sub)

	con.cerrarConexion()

	if tareas is None:

		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tareas no existentes")

	return obtenerObjetosTarea(tareas)


@router_tareas.get("/{id_tarea}", status_code=status.HTTP_200_OK, summary="Devuelve los datos de la tarea")
async def obtenerTarea(id_tarea:str=Path(..., title="Id de la tarea", description="El id de la tarea que quieres obtener"),
						payload:Payload=Depends(decodificarToken),
						con:Conexion=Depends(crearConexion))->Tarea:

	"""
	Devuelve el diccionario de los datos de la tarea.

	## Parametros

	- **Id_tarea**: El id de la tarea (str).

	200 (OK): Si se obtiene la tarea correctamente

	- **Id_tarea**: El id de la tarea (str).
	- **Titulo**: El titulo de la tarea (str).
	- **Descripcion**: La descripcion de la tarea (str).
	- **Categoria**: La categoria de la tarea (str).
	- **Completada**: El estado de la tarea (bool).
	- **Comentario**: El comentario de la tarea (str).
	- **Fecha_creacion**: La fecha de creacion de la tarea (str).
	- **Fecha_completada**: La fecha de la realizacion de la tarea (str).

	401 (UNAUTHORIZED): Si los datos no son correctos

	- **Mensaje**: El mensaje de la excepcion (str).

	404 (NOT FOUND): Si no se obtiene la tarea correctamente

	- **Mensaje**: El mensaje de la excepcion (str).
	"""

	tarea=con.obtenerDatosTarea(id_tarea)

	if tarea is None:

		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no existente")

	return obtenerObjetoTarea(tarea)
	