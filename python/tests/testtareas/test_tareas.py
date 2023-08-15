import pytest
from typing import Dict
from fastapi.testclient import TestClient 


# Funcion para obtener el header y poder acceder
def obtenerHeaderToken(objeto_cliente:TestClient)->Dict:

	objeto_cliente.post("/usuarios", json={"usuario":"nacho98", "nombre":"Nacho", "apellido1":"Dorado", "apellido2":"Ruiz", "contrasena":"1234567891", "edad":25, "ciudad":"Madrid", "pais":"España"})

	datos_form={"grant_type": "password", "username": "nacho98", "password": "1234567891", "scope": "", "client_id": "", "client_secret": ""}

	contenido_token=objeto_cliente.post("/tokens", data=datos_form).json()

	token=contenido_token["access_token"]

	return {"Authorization": f"Bearer {token}"}




@pytest.mark.parametrize(["token"],
	[("token",), ("dgfdkjg89e5yujgfkjgdf",), ("nacho98",), ("amanditaa",), ("1234",)]
)
def test_pagina_agregar_tarea_no_autenticado(cliente, token):

	header={"Authorization": f"Bearer {token}"}

	respuesta=cliente.post("/tareas", headers=header, json={"titulo":"Titulo", "descripcion":"Descripcion", "categoria":"Categoria"})

	contenido=respuesta.json()

	assert respuesta.status_code==401
	assert "detail" in contenido


@pytest.mark.parametrize(["tarea"],
	[
		({"titulo":"Titulo", "descripcion":"Descripcion", "categoria":25},),
		({"titulo":"Titulo", "descripcion":"Descripcion"},),
		({"descripcion":"Descripcion", "categoria":"Categoria"},),
		({"titulo":"Titulo"},),
		({},),
	]
)
def test_pagina_agregar_tarea_autenticado_incorrecto(cliente, conexion, tarea):

	header=obtenerHeaderToken(cliente)

	respuesta=cliente.post("/tareas", json=tarea, headers=header)

	contenido=respuesta.json()

	assert respuesta.status_code==422
	assert not "mensaje" in contenido
	assert not "tarea" in contenido

	conexion.c.execute("SELECT * FROM tareas")

	assert len(conexion.c.fetchall())==0


def test_pagina_agregar_tarea_autenticado(cliente, conexion):

	header=obtenerHeaderToken(cliente)

	respuesta=cliente.post("/tareas", json={"titulo":"Titulo", "descripcion":"Descripcion", "categoria":"Categoria"}, headers=header)

	contenido=respuesta.json()

	assert respuesta.status_code==201
	assert "mensaje" in contenido
	assert "tarea" in contenido
	assert "titulo" in contenido["tarea"]
	assert "descripcion" in contenido["tarea"]

	conexion.c.execute("SELECT * FROM tareas")

	assert len(conexion.c.fetchall())==1


def test_pagina_agregar_tareas_autenticado(cliente, conexion):

	header=obtenerHeaderToken(cliente)

	cliente.post("/tareas", json={"titulo":"Titulo", "descripcion":"Descripcion", "categoria":"Categoria"}, headers=header)
	cliente.post("/tareas", json={"titulo":"Titulo", "descripcion":"Descripcion", "categoria":"Categoria"}, headers=header)
	cliente.post("/tareas", json={"titulo":"Titulo", "descripcion":"Descripcion", "categoria":"Categoria"}, headers=header)

	conexion.c.execute("SELECT * FROM tareas")

	assert len(conexion.c.fetchall())==3


@pytest.mark.parametrize(["token"],
	[("token",), ("dgfdkjg89e5yujgfkjgdf",), ("nacho98",), ("amanditaa",), ("1234",)]
)
def test_pagina_obtener_tareas_no_autenticado(cliente, token):

	header={"Authorization": f"Bearer {token}"}

	respuesta=cliente.get("/tareas", headers=header)

	contenido=respuesta.json()

	assert respuesta.status_code==401
	assert "detail" in contenido

def test_pagina_obtener_tareas_autenticado_no_existentes(cliente, conexion):

	header=obtenerHeaderToken(cliente)

	respuesta=cliente.get("/tareas", headers=header)

	contenido=respuesta.json()

	assert respuesta.status_code==404
	assert "detail" in contenido

def test_pagina_obtener_tareas_autenticado_existentes(cliente, conexion):

	header=obtenerHeaderToken(cliente)

	cliente.post("/tareas", json={"titulo":"Titulo", "descripcion":"Descripcion", "categoria":"Categoria"}, headers=header)
	cliente.post("/tareas", json={"titulo":"Titulo", "descripcion":"Descripcion", "categoria":"Categoria"}, headers=header)
	cliente.post("/tareas", json={"titulo":"Titulo", "descripcion":"Descripcion", "categoria":"Categoria"}, headers=header)

	respuesta=cliente.get("/tareas", headers=header)

	contenido=respuesta.json()

	assert respuesta.status_code==200
	assert len(contenido)==3


@pytest.mark.parametrize(["token"],
	[("token",), ("dgfdkjg89e5yujgfkjgdf",), ("nacho98",), ("amanditaa",), ("1234",)]
)
def test_pagina_obtener_tarea_no_autenticado(cliente, token):

	header={"Authorization": f"Bearer {token}"}

	respuesta=cliente.get("/tareas/1", headers=header)

	contenido=respuesta.json()

	assert respuesta.status_code==401
	assert "detail" in contenido

def test_pagina_obtener_tarea_autenticado_no_existentes(cliente, conexion):

	header=obtenerHeaderToken(cliente)

	respuesta=cliente.get("/tareas/1", headers=header)

	contenido=respuesta.json()

	assert respuesta.status_code==404
	assert "detail" in contenido

def test_pagina_obtener_tarea_autenticado_existente(cliente, conexion):

	header=obtenerHeaderToken(cliente)

	cliente.post("/tareas", json={"titulo":"Titulo", "descripcion":"Descripcion", "categoria":"Categoria"}, headers=header)

	conexion.c.execute("SELECT id_tarea FROM tareas")

	id_tarea=conexion.c.fetchone()["id_tarea"]

	respuesta=cliente.get(f"/tareas/{id_tarea}", headers=header)

	contenido=respuesta.json()

	assert respuesta.status_code==200
	assert "id_tarea" in contenido
	assert "titulo" in contenido
	assert "descripcion" in contenido
	assert "categoria" in contenido
	assert "completada" in contenido
	assert "comentario" in contenido
	assert "fecha_creacion" in contenido
	assert "fecha_completada" in contenido
	