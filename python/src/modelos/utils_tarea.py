from typing import Dict, List

from .tarea import Tarea

# Funcion para obtener un objeto tarea
def obtenerObjetoTarea(valores:Dict)->Tarea:

	
	fecha_creacion=valores["fecha_creacion"].strftime("%Y-%m-%d")

	# La fecha completada puede ser None
	try:

		fecha_completada=valores["fecha_completada"].strftime("%Y-%m-%d")

	except AttributeError as e:

		fecha_completada=valores["fecha_completada"]

	return Tarea(id_tarea=valores["id_tarea"],
				titulo=valores["titulo"],
				descripcion=valores["descripcion"],
				categoria=valores["categoria"],
				completada=valores["completada"],
				comentario=valores["comentario"],
				fecha_creacion=fecha_creacion,
				fecha_completada=fecha_completada)

# Funcion para obtener varios objetos tarea
def obtenerObjetosTarea(lista_valores:List[Dict])->List[Tarea]:

	return [obtenerObjetoTarea(valor) for valor in lista_valores]