from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re
import pandas as pd



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173"],  # Permite las solicitudes desde este origen
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP
    allow_headers=["*"],  # Permite todos los headers HTTP
)

df = pd.read_excel('datospersonales.xlsx')

class SearchData(BaseModel):
    campo: str
    valor: str

class UserData(BaseModel):
    email: str
    password: str

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/register")
def register(user: UserData):
    try:
        return {"message": "User created"}
    except:
        raise HTTPException(status_code=400, detail="Failed to create user")

@app.post("/search")
def search(data: SearchData):
    # Convertir los valores a minúsculas para una búsqueda insensible a mayúsculas y minúsculas
    valor_minuscula = data.valor.lower()
    campo_minuscula = df[data.campo].str.lower()

    # Filtrar los registros que comienzan exactamente con el valor en el campo especificado
    registros = df[campo_minuscula.str.contains(valor_minuscula, na=False)]

    # Si no se encontraron registros, regresar un mensaje indicando esto
    if registros.empty:
        raise HTTPException(status_code=404, detail="No se encontraron registros")

    # Convertir los registros a un tipo que sea serializable en JSON
    registros_json = registros.astype(str).to_dict(orient='records')

    # Si se encontraron registros, regresar estos
    return registros_json
