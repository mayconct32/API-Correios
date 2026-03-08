from fastapi import FastAPI
from src.correios_cep.controller.correios_controller import app as correios


app = FastAPI()


app.include_router(correios)