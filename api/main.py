from fastapi import FastAPI
from .routers import basic, advanced


app = FastAPI()

app.include_router(basic.router)
app.include_router(advanced.router)





