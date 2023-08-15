import pytest

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

def test_obtener_tareas_no_existen(conexion):

	conexion.insertarUsuario("nacho98", "nacho", "dorado", "ruiz", "1234", 25, "madrid", "españa")

	assert conexion.obtenerTareas("nacho98") is None

def test_obtener_tareas_existen(conexion):

	conexion.insertarUsuario("nacho98", "nacho", "dorado", "ruiz", "1234", 25, "madrid", "españa")

	conexion.insertarTarea("idtarea", "nacho98", "titulo", "descripcion", "categoria", "2023-08-13")
	conexion.insertarTarea("idtarea2", "nacho98", "titulo", "descripcion", "categoria", "2023-08-13")
	conexion.insertarTarea("idtarea3", "nacho98", "titulo", "descripcion", "categoria", "2023-08-13")

	tareas=conexion.obtenerTareas("nacho98")

	assert len(tareas)==3

	for tarea in tareas:

		assert "id_tarea" in tarea
		assert "titulo" in tarea
		assert "descripcion" in tarea
		assert "categoria" in tarea
		assert "completada" in tarea
		assert "comentario" in tarea
		assert "fecha_creacion" in tarea
		assert "fecha_completada" in tarea

@pytest.mark.parametrize(["id_tarea"],
	[("1",),("gdskgdsjkfgjk",),("id",),("tarea",),("id_tarea",)]
)
def test_obtener_tarea_no_existen(conexion, id_tarea):

	conexion.insertarUsuario("nacho98", "nacho", "dorado", "ruiz", "1234", 25, "madrid", "españa")

	conexion.insertarTarea("idtarea", "nacho98", "titulo", "descripcion", "categoria", "2023-08-13")

	assert conexion.obtenerDatosTarea(id_tarea) is None

def test_obtener_tarea_existen(conexion):

	conexion.insertarUsuario("nacho98", "nacho", "dorado", "ruiz", "1234", 25, "madrid", "españa")

	conexion.insertarTarea("idtarea", "nacho98", "titulo", "descripcion", "categoria", "2023-08-13")

	tarea=conexion.obtenerDatosTarea("idtarea")

	assert "id_tarea" in tarea
	assert "titulo" in tarea
	assert "descripcion" in tarea
	assert "categoria" in tarea
	assert "completada" in tarea
	assert "comentario" in tarea
	assert "fecha_creacion" in tarea
	assert "fecha_completada" in tarea