import pytest

@pytest.mark.parametrize(["usuario"],
	[
		({"usuario":"nacho98", "nombre":"Nacho", "apellido1":"Dorado", "apellido2":"Ruiz", "contrasena":"12345678", "edad":"a", "ciudad":"Madrid", "pais":"España"},),
		({"usuario":"nacho98", "nombre":"Nacho", "apellido1":"Dorado", "apellido2":"Ruiz", "contrasena":"12345678", "edad":17, "ciudad":"Madrid", "pais":"España"},),
		({"usuario":"nacho98", "nombre":"Nacho", "apellido1":"Dorado", "apellido2":"Ruiz", "contrasena":"12345678", "edad":100, "ciudad":"Madrid", "pais":"España"},),
		({"usuario":"nacho98", "nombre":"Nacho", "apellido1":"Dorado", "apellido2":"Ruiz", "contrasena":"123456789", "edad":25, "ciudad":"Madrid", "pais":"España"},),
		({"usuario":"nacho98", "nombre":"Nacho", "apellido1":"Dorado", "apellido2":"Ruiz", "contrasena":"1234567 89", "edad":25, "ciudad":"Madrid", "pais":"España"},),
		({"nombre":"Nacho", "apellido1":"Dorado", "apellido2":"Ruiz", "contrasena":"1234567", "edad":25, "ciudad":"Madrid", "pais":"España"},),
		({"usuario":"nacho98", "nombre":"Nacho", "apellido1":"Dorado", "apellido2":"Ruiz", "contrasena":"1234567"},),
		({"usuario":"nacho98"},)
	]
)
def test_pagina_agregar_usuario_incorrecto(cliente, conexion, usuario):

	respuesta=cliente.post("/usuarios", json=usuario)

	contenido=respuesta.json()

	assert respuesta.status_code==422
	assert not "mensaje" in contenido
	assert not "usuario" in contenido

	conexion.c.execute("SELECT * FROM usuarios")

	assert len(conexion.c.fetchall())==0


def test_pagina_agregar_usuario_existente(cliente, conexion):

	conexion.insertarUsuario("nacho98", "Nacho", "Dorado", "Ruiz", "12345678", 25, "Madrid", "España")

	conexion.c.execute("SELECT * FROM usuarios")

	assert len(conexion.c.fetchall())==1

	respuesta=cliente.post("/usuarios", json={"usuario":"nacho98", "nombre":"Nacho", "apellido1":"Dorado", "apellido2":"Ruiz", "contrasena":"12345678", "edad":25, "ciudad":"Madrid", "pais":"España"})

	contenido=respuesta.json()

	assert respuesta.status_code==400
	assert "detail" in contenido

	conexion.c.execute("SELECT * FROM usuarios")

	assert len(conexion.c.fetchall())==1


def test_pagina_agregar_usuario(cliente, conexion):

	respuesta=cliente.post("/usuarios", json={"usuario":"nacho98", "nombre":"Nacho", "apellido1":"Dorado", "apellido2":"Ruiz", "contrasena":"12345678", "edad":25, "ciudad":"Madrid", "pais":"España"})

	contenido=respuesta.json()

	assert respuesta.status_code==201
	assert "mensaje" in contenido
	assert "usuario" in contenido
	assert "usuario" in contenido["usuario"]
	assert "nombre" in contenido["usuario"]

	conexion.c.execute("SELECT * FROM usuarios")

	assert len(conexion.c.fetchall())==1

def test_pagina_agregar_usuarios(cliente, conexion):

	cliente.post("/usuarios", json={"usuario":"nacho98", "nombre":"Nacho", "apellido1":"Dorado", "apellido2":"Ruiz", "contrasena":"12345678", "edad":25, "ciudad":"Madrid", "pais":"España"})
	cliente.post("/usuarios", json={"usuario":"nacho99", "nombre":"Nacho", "apellido1":"Dorado", "apellido2":"Ruiz", "contrasena":"12345678", "edad":25, "ciudad":"Madrid", "pais":"España"})
	cliente.post("/usuarios", json={"usuario":"nacho989", "nombre":"Nacho", "apellido1":"Dorado", "apellido2":"Ruiz", "contrasena":"12345678", "edad":25, "ciudad":"Madrid", "pais":"España"})

	conexion.c.execute("SELECT * FROM usuarios")

	assert len(conexion.c.fetchall())==3


def test_pagina_obtener_usuarios_no_existentes(cliente, conexion):

	respuesta=cliente.get("/usuarios")

	contenido=respuesta.json()

	assert respuesta.status_code==404
	assert "detail" in contenido


def test_pagina_obtener_usuarios_existentes(cliente, conexion):

	cliente.post("/usuarios", json={"usuario":"nacho98", "nombre":"Nacho", "apellido1":"Dorado", "apellido2":"Ruiz", "contrasena":"12345678", "edad":25, "ciudad":"Madrid", "pais":"España"})
	cliente.post("/usuarios", json={"usuario":"nacho99", "nombre":"Nacho", "apellido1":"Dorado", "apellido2":"Ruiz", "contrasena":"12345678", "edad":25, "ciudad":"Madrid", "pais":"España"})
	cliente.post("/usuarios", json={"usuario":"nacho989", "nombre":"Nacho", "apellido1":"Dorado", "apellido2":"Ruiz", "contrasena":"12345678", "edad":25, "ciudad":"Madrid", "pais":"España"})

	respuesta=cliente.get("/usuarios")

	contenido=respuesta.json()

	assert respuesta.status_code==200
	assert len(contenido)==3


@pytest.mark.parametrize(["token"],
	[("token",), ("dgfdkjg89e5yujgfkjgdf",), ("nacho98",), ("amanditaa",), ("1234",)]
)
def test_pagina_obtener_datos_usuario_no_autenticado(cliente, token):

	header={"Authorization": f"Bearer {token}"}

	respuesta=cliente.get("/usuarios/me", headers=header)

	contenido=respuesta.json()

	assert respuesta.status_code==401
	assert "detail" in contenido


@pytest.mark.parametrize(["usuario", "contrasena"],
	[
		("nacho98", "1234567891"),
		("nacho98", "qwertyuiop"),
		("amanda99", "1q2w3e4r5t6y7u"),

	]
)
def test_pagina_obtener_datos_usuario_autenticado(cliente, conexion, usuario, contrasena):

	cliente.post("/usuarios", json={"usuario":usuario, "nombre":"Nacho", "apellido1":"Dorado", "apellido2":"Ruiz", "contrasena":contrasena, "edad":25, "ciudad":"Madrid", "pais":"España"})

	datos_form={"grant_type": "password", "username": usuario, "password": contrasena, "scope": "", "client_id": "", "client_secret": ""}

	contenido_token=cliente.post("/tokens", data=datos_form).json()

	token=contenido_token["access_token"]

	header={"Authorization": f"Bearer {token}"}

	respuesta=cliente.get("/usuarios/me", headers=header)

	contenido=respuesta.json()

	assert respuesta.status_code==200
	assert "usuario" in contenido
	assert "nombre" in contenido
	assert "apellido1" in contenido
	assert "apellido2" in contenido
	assert "edad" in contenido
	assert "ciudad" in contenido
	assert "pais" in contenido


