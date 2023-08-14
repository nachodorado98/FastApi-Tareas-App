from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TareaBBDD(BaseModel):

	titulo:str
	descripcion:str
	categoria:str

	class Config:

		json_schema_extra={"example":{"titulo":"Tarea",
										"descripcion":"La descripcion de la tarea",
										"categoria":"Ocio"}}

class Tarea(TareaBBDD):

	id_tarea:str
	completada:bool
	comentario:Optional[str]
	fecha_creacion:str
	fecha_completada:Optional[str]