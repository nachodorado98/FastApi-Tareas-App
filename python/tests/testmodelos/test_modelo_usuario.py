import pytest

from src.modelos.usuario import UsuarioBBDD


@pytest.mark.parametrize(["usuario"],
	[
		({"usuario":"nacho98", "nombre":"Nacho", "apellido1":"Dorado", "apellido2":"Ruiz", "contrasena":"12345678", "edad":"a", "ciudad":"Madrid", "pais":"España"},),
		({"usuario":"nacho98", "nombre":"Nacho", "apellido1":"Dorado", "apellido2":"Ruiz", "contrasena":"12345678", "edad":17, "ciudad":"Madrid", "pais":"España"},),
		({"usuario":"nacho98", "nombre":"Nacho", "apellido1":"Dorado", "apellido2":"Ruiz", "contrasena":"12345678", "edad":100, "ciudad":"Madrid", "pais":"España"},),
		({"usuario":"nacho98", "nombre":"Nacho", "apellido1":"Dorado", "apellido2":"Ruiz", "contrasena":"123456789", "edad":25, "ciudad":"Madrid", "pais":"España"},),
		({"usuario":"nacho98", "nombre":"Nacho", "apellido1":"Dorado", "apellido2":"Ruiz", "contrasena":"1234567 89", "edad":25, "ciudad":"Madrid", "pais":"España"},),
		({"usuario":"nacho98", "nombre":"Nacho", "apellido1":"Dorado", "apellido2":"Ruiz", "contrasena":"1234567", "edad":25, "ciudad":"Madrid", "pais":"España"},)
	]
)
def test_modelo_usuario_bbdd_incorrecto(usuario):

	with pytest.raises(ValueError):

		UsuarioBBDD(**usuario)