from pydantic import BaseModel, validator

class Usuario(BaseModel):

	usuario:str
	nombre:str
	apellido1:str
	apellido2:str
	edad:int
	ciudad:str
	pais:str

class UsuarioBBDD(Usuario):

	contrasena:str

	@validator("edad")
	def comprobarEdad(cls, edad:int)->int:

		if edad<18 or edad>99:

			raise ValueError("la edad no esta dentro del rango")

		return edad

	@validator("contrasena")
	def comprobarContrasena(cls, contrasena:str)->str:

		if len(contrasena)<8 or " " in contrasena or contrasena=="123456789":

			raise ValueError("la contraseña no cumple los requisitos")

		return contrasena

	class Config:

		json_schema_extra={"example":{"usuario":"nacho98",
										"nombre":"Nacho",
										"apellido1":"Dorado",
										"apellido2":"Ruiz",
										"contrasena":"123456789",
										"edad":25,
										"ciudad":"Madrid",
										"pais":"España"}}