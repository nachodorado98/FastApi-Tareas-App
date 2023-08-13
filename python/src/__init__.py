from fastapi import FastAPI

from .metadata.confmetadata import *
from .routers.inicio import router_inicio
from .routers.usuarios import router_usuarios
from .autenticacion.auth import router_auth
from .routers.tareas import router_tareas

# Funcion para crear la app
def crear_app():

	app=FastAPI(title=TITULO,
				description=DESCRIPCION,
				version=VERSION,
				contact=CONTACTO,
				license_info=LICENCIA)

	app.include_router(router_inicio)
	app.include_router(router_usuarios)
	app.include_router(router_auth)
	app.include_router(router_tareas)
	
	return app