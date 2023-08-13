def test_tabla_usuario_vacia(conexion):

	conexion.c.execute("SELECT * FROM tareas")

	assert conexion.c.fetchall()==[]

def test_insertar_tarea(conexion):

	conexion.insertarUsuario("nacho98", "nacho", "dorado", "ruiz", "1234", 25, "madrid", "españa")

	conexion.insertarTarea("idtarea", "nacho98", "titulo", "descripcion", "categoria", "2023-08-13")

	conexion.c.execute("SELECT * FROM tareas")

	assert len(conexion.c.fetchall())==1

def test_insertar_usuarios(conexion):

	conexion.insertarUsuario("nacho98", "nacho", "dorado", "ruiz", "1234", 25, "madrid", "españa")

	conexion.insertarTarea("idtarea", "nacho98", "titulo", "descripcion", "categoria", "2023-08-13")
	conexion.insertarTarea("idtarea2", "nacho98", "titulo", "descripcion", "categoria", "2023-08-13")
	conexion.insertarTarea("idtarea3", "nacho98", "titulo", "descripcion", "categoria", "2023-08-13")

	conexion.c.execute("SELECT * FROM tareas")

	assert len(conexion.c.fetchall())==3
