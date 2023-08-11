from src.modelos.usuario import UsuarioBasico
from src.modelos.utils_usuario import obtenerObjetoUsuarioBasico, obtenerObjetosUsuarioBasico

def test_obtener_usuario_basico():

	usuario={"nombre":"Nacho", "apellido1":"Dorado"}

	objeto=obtenerObjetoUsuarioBasico(usuario)

	assert isinstance(objeto, UsuarioBasico)
	assert objeto.nombre=="Nacho"
	assert objeto.apellido1=="Dorado"


def test_obtener_varios_usuarios_basicos():

	usuarios=[{"nombre":"Nacho", "apellido1":"Dorado"},
			{"nombre":"Nacho", "apellido1":"Dorado"},
			{"nombre":"Nacho", "apellido1":"Dorado"}]

	objetos=obtenerObjetosUsuarioBasico(usuarios)

	assert len(objetos)==3

	for objeto in objetos:

		assert isinstance(objeto, UsuarioBasico)
		assert objeto.nombre=="Nacho"
		assert objeto.apellido1=="Dorado"
