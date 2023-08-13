import os
import sys
sys.path.append("..")

import pytest
from fastapi.testclient import TestClient 

from src import crear_app
from src.database.conexion import Conexion

@pytest.fixture()
def app():

	app=crear_app()

	return app


@pytest.fixture()
def cliente(app):

	return TestClient(app)


@pytest.fixture()
def conexion(app):

	con=Conexion()

	con.c.execute("DELETE FROM usuarios")

	con.c.execute("DELETE FROM tareas")

	con.bbdd.commit()

	return con