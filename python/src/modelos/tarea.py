from pydantic import BaseModel

class TareaBBDD(BaseModel):

	titulo:str
	descripcion:str
	categoria:str

	class Config:

		json_schema_extra={"example":{"titulo":"Tarea",
										"descripcion":"La descripcion de la tarea",
										"categoria":"Ocio"}}