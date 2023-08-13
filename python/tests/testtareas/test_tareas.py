import pytest

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

	cliente.post("/usuarios", json={"usuario":"nacho98", "nombre":"Nacho", "apellido1":"Dorado", "apellido2":"Ruiz", "contrasena":"1234567891", "edad":25, "ciudad":"Madrid", "pais":"España"})

	datos_form={"grant_type": "password", "username": "nacho98", "password": "1234567891", "scope": "", "client_id": "", "client_secret": ""}

	contenido_token=cliente.post("/tokens", data=datos_form).json()

	token=contenido_token["access_token"]

	header={"Authorization": f"Bearer {token}"}

	respuesta=cliente.post("/tareas", json=tarea, headers=header)

	contenido=respuesta.json()

	assert respuesta.status_code==422
	assert not "mensaje" in contenido
	assert not "tarea" in contenido

	conexion.c.execute("SELECT * FROM tareas")

	assert len(conexion.c.fetchall())==0


def test_pagina_agregar_tarea_autenticado(cliente, conexion):

	cliente.post("/usuarios", json={"usuario":"nacho98", "nombre":"Nacho", "apellido1":"Dorado", "apellido2":"Ruiz", "contrasena":"1234567891", "edad":25, "ciudad":"Madrid", "pais":"España"})

	datos_form={"grant_type": "password", "username": "nacho98", "password": "1234567891", "scope": "", "client_id": "", "client_secret": ""}

	contenido_token=cliente.post("/tokens", data=datos_form).json()

	token=contenido_token["access_token"]

	header={"Authorization": f"Bearer {token}"}

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

	cliente.post("/usuarios", json={"usuario":"nacho98", "nombre":"Nacho", "apellido1":"Dorado", "apellido2":"Ruiz", "contrasena":"1234567891", "edad":25, "ciudad":"Madrid", "pais":"España"})

	datos_form={"grant_type": "password", "username": "nacho98", "password": "1234567891", "scope": "", "client_id": "", "client_secret": ""}

	contenido_token=cliente.post("/tokens", data=datos_form).json()

	token=contenido_token["access_token"]

	header={"Authorization": f"Bearer {token}"}

	cliente.post("/tareas", json={"titulo":"Titulo", "descripcion":"Descripcion", "categoria":"Categoria"}, headers=header)
	cliente.post("/tareas", json={"titulo":"Titulo", "descripcion":"Descripcion", "categoria":"Categoria"}, headers=header)
	cliente.post("/tareas", json={"titulo":"Titulo", "descripcion":"Descripcion", "categoria":"Categoria"}, headers=header)

	conexion.c.execute("SELECT * FROM tareas")

	assert len(conexion.c.fetchall())==3