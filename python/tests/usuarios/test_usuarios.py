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
def test_agregar_usuario_incorrecto(cliente, conexion, usuario):

	respuesta=cliente.post("/usuarios", json=usuario)

	contenido=respuesta.json()

	assert respuesta.status_code==422
	assert not "mensaje" in contenido
	assert not "usuario" in contenido

	conexion.c.execute("SELECT * FROM usuarios")

	assert len(conexion.c.fetchall())==0


def test_agregar_usuario_existente(cliente, conexion):

	conexion.insertarUsuario("nacho98", "Nacho", "Dorado", "Ruiz", "12345678", 25, "Madrid", "España")

	conexion.c.execute("SELECT * FROM usuarios")

	assert len(conexion.c.fetchall())==1

	respuesta=cliente.post("/usuarios", json={"usuario":"nacho98", "nombre":"Nacho", "apellido1":"Dorado", "apellido2":"Ruiz", "contrasena":"12345678", "edad":25, "ciudad":"Madrid", "pais":"España"})

	contenido=respuesta.json()

	assert respuesta.status_code==400
	assert "detail" in contenido

	conexion.c.execute("SELECT * FROM usuarios")

	assert len(conexion.c.fetchall())==1


def test_agregar_usuario(cliente, conexion):

	respuesta=cliente.post("/usuarios", json={"usuario":"nacho98", "nombre":"Nacho", "apellido1":"Dorado", "apellido2":"Ruiz", "contrasena":"12345678", "edad":25, "ciudad":"Madrid", "pais":"España"})

	contenido=respuesta.json()

	assert respuesta.status_code==201
	assert "mensaje" in contenido
	assert "usuario" in contenido
	assert "usuario" in contenido["usuario"]
	assert "nombre" in contenido["usuario"]

	conexion.c.execute("SELECT * FROM usuarios")

	assert len(conexion.c.fetchall())==1

def test_agregar_usuarios(cliente, conexion):

	cliente.post("/usuarios", json={"usuario":"nacho98", "nombre":"Nacho", "apellido1":"Dorado", "apellido2":"Ruiz", "contrasena":"12345678", "edad":25, "ciudad":"Madrid", "pais":"España"})
	cliente.post("/usuarios", json={"usuario":"nacho99", "nombre":"Nacho", "apellido1":"Dorado", "apellido2":"Ruiz", "contrasena":"12345678", "edad":25, "ciudad":"Madrid", "pais":"España"})
	cliente.post("/usuarios", json={"usuario":"nacho989", "nombre":"Nacho", "apellido1":"Dorado", "apellido2":"Ruiz", "contrasena":"12345678", "edad":25, "ciudad":"Madrid", "pais":"España"})

	conexion.c.execute("SELECT * FROM usuarios")

	assert len(conexion.c.fetchall())==3