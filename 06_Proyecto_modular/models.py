from pydantic import BaseModel

class UsuarioModelo(BaseModel):
    username: str
    password: str