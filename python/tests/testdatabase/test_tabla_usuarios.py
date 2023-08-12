import pytest

def test_tabla_usuario_vacia(conexion):

	conexion.c.execute("SELECT * FROM usuarios")

	assert conexion.c.fetchall()==[]

def test_insertar_usuario(conexion):

	conexion.insertarUsuario("nacho98", "nacho", "dorado", "ruiz", "1234", 25, "madrid", "españa")

	conexion.c.execute("SELECT * FROM usuarios")

	assert len(conexion.c.fetchall())==1

def test_insertar_usuarios(conexion):

	conexion.insertarUsuario("nacho98", "nacho", "dorado", "ruiz", "1234", 25, "madrid", "españa")
	conexion.insertarUsuario("nacho99", "nacho", "dorado", "ruiz", "1234", 25, "madrid", "españa")
	conexion.insertarUsuario("nacho989", "nacho", "dorado", "ruiz", "1234", 25, "madrid", "españa")

	conexion.c.execute("SELECT * FROM usuarios")

	assert len(conexion.c.fetchall())==3

def test_usuario_no_existe(conexion):

	assert not conexion.existe_usuario("nacho98")

	conexion.insertarUsuario("nacho99", "nacho", "dorado", "ruiz", "1234", 25, "madrid", "españa")

	assert not conexion.existe_usuario("nacho98")

def test_usuario_existe(conexion):

	assert not conexion.existe_usuario("nacho98")

	conexion.insertarUsuario("nacho98", "nacho", "dorado", "ruiz", "1234", 25, "madrid", "españa")

	assert conexion.existe_usuario("nacho98")

def test_obtener_usuarios_no_existen(conexion):

	assert conexion.obtenerUsuarios() is None

def test_obtener_usuarios_existen(conexion):

	conexion.insertarUsuario("nacho98", "nacho", "dorado", "ruiz", "1234", 25, "madrid", "españa")
	conexion.insertarUsuario("nacho99", "nacho", "dorado", "ruiz", "1234", 25, "madrid", "españa")
	conexion.insertarUsuario("nacho989", "nacho", "dorado", "ruiz", "1234", 25, "madrid", "españa")

	usuarios=conexion.obtenerUsuarios()

	assert len(usuarios)==3

	for usuario in usuarios:

		assert "nombre" in usuario
		assert "apellido1" in usuario

def test_obtener_contrasena_usuario_no_existe(conexion):

	assert conexion.obtenerContrasena("nacho98") is None

@pytest.mark.parametrize(["usuario"],
	[("nacho98",),("nacho99",),("nacho989",)]
)
def test_obtener_contrasena_usuario_existe(conexion, usuario):

	conexion.insertarUsuario("nacho98", "nacho", "dorado", "ruiz", "1234", 25, "madrid", "españa")
	conexion.insertarUsuario("nacho99", "nacho", "dorado", "ruiz", "1234", 25, "madrid", "españa")
	conexion.insertarUsuario("nacho989", "nacho", "dorado", "ruiz", "1234", 25, "madrid", "españa")

	contrasena=conexion.obtenerContrasena(usuario)

	assert contrasena=="1234"

def test_obtener_datos_usuario_no_existe(conexion):

	assert conexion.obtenerDatosUsuario("nacho98") is None

def test_obtener_datos_usuario_existe(conexion):

	conexion.insertarUsuario("nacho98", "nacho", "dorado", "ruiz", "1234", 25, "madrid", "españa")

	datos=conexion.obtenerDatosUsuario("nacho98")

	assert datos["usuario"]=="nacho98"
	assert datos["nombre"]=="nacho"
	assert datos["apellido1"]=="dorado"
	assert datos["apellido2"]=="ruiz"
	assert datos["edad"]==25
	assert datos["ciudad"]=="madrid"
	assert datos["pais"]=="españa"
	assert "contrasena" not in datos

	

