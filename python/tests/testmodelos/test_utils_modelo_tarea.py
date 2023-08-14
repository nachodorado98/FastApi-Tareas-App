import pytest
import datetime

from src.modelos.tarea import Tarea
from src.modelos.utils_tarea import obtenerObjetoTarea, obtenerObjetosTarea

@pytest.mark.parametrize(["tarea"],
	[
		({"id_tarea":"qwertyuiop", "titulo":"Titulo", "descripcion":"Descripcion", "categoria":"Categoria", "completada":False, "comentario":None, "fecha_creacion":datetime.date(2023,8,13), "fecha_completada":None},),
		({"id_tarea":"qwertyuiop", "titulo":"Titulo", "descripcion":"Descripcion", "categoria":"Categoria", "completada":False, "comentario":None, "fecha_creacion":datetime.date(2023,8,13), "fecha_completada":datetime.date(2023,8,13)},),
		({"id_tarea":"qwertyuiop", "titulo":"Titulo", "descripcion":"Descripcion", "categoria":"Categoria", "completada":True, "comentario":"Comentario", "fecha_creacion":datetime.date(2023,8,13), "fecha_completada":None},),
		({"id_tarea":"qwertyuiop", "titulo":"Titulo", "descripcion":"Descripcion", "categoria":"Categoria", "completada":True, "comentario":None, "fecha_creacion":datetime.date(2023,8,13), "fecha_completada":None},)
	]
)
def test_obtener_tarea(tarea):

	objeto=obtenerObjetoTarea(tarea)

	assert isinstance(objeto, Tarea)
	assert objeto.id_tarea==tarea["id_tarea"]
	assert objeto.completada==tarea["completada"]
	assert objeto.comentario==tarea["comentario"]


def test_obtener_varias_tareas():

	tareas=[{"id_tarea":"qwertyuiop", "titulo":"Titulo", "descripcion":"Descripcion", "categoria":"Categoria", "completada":False, "comentario":None, "fecha_creacion":datetime.date(2023,8,13), "fecha_completada":None},
			{"id_tarea":"qwertyuiop", "titulo":"Titulo", "descripcion":"Descripcion", "categoria":"Categoria", "completada":True, "comentario":None, "fecha_creacion":datetime.date(2023,8,13), "fecha_completada":None},
			{"id_tarea":"qwertyuiop", "titulo":"Titulo", "descripcion":"Descripcion", "categoria":"Categoria", "completada":False, "comentario":"Comentario", "fecha_creacion":datetime.date(2023,8,13), "fecha_completada":None},
			{"id_tarea":"qwertyuiop", "titulo":"Titulo", "descripcion":"Descripcion", "categoria":"Categoria", "completada":False, "comentario":None, "fecha_creacion":datetime.date(2023,8,13), "fecha_completada":datetime.date(2023,8,13)}]

	objetos=obtenerObjetosTarea(tareas)

	assert len(objetos)==4

	for objeto in objetos:

		assert isinstance(objeto, Tarea)
