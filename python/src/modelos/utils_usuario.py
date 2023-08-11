from typing import Dict, List

from .usuario import UsuarioBasico

# Funcion para obtener un objeto usuario basico
def obtenerObjetoUsuarioBasico(valores:Dict)->UsuarioBasico:

	return UsuarioBasico(**valores)

# Funcion para obtener varios objetos usuario basico
def obtenerObjetosUsuarioBasico(lista_valores:List[Dict])->List[UsuarioBasico]:

	return [obtenerObjetoUsuarioBasico(valor) for valor in lista_valores]