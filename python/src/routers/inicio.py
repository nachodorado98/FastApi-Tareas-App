from fastapi import APIRouter, status
from typing import Dict


router_inicio=APIRouter(tags=["Inicio"])


@router_inicio.get("/", status_code=status.HTTP_200_OK, summary="Devuelve informacion de la API")
async def inicio()->Dict:

	"""
    Devuelve un diccionario con la informacion de la API.

    ## Respuesta

    200 (OK): Si se obtiene el mensaje de informacion correctamente

    - **Mensaje**: El mensaje de bienvenida (str).
    - **Version**: La version de la API (str).
    - **Descripcion**: La descripcion de la finalidad de la API (str).
    - **Documentacion**: La direccion de la documentacion de la API (str).
    """

	return {"mensaje": "¡Bienvenido a la REST API de Tareas con FastAPI!",
			"version": "1.0.0",
			"descripcion": "Esta API permite realizar operaciones con usuarios y tareas. Todos los usuarios y tareas se guardan en una base de datos PostgreSQL.",
			"documentacion": "/docs"}
