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

