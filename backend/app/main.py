# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="ARES 2.0 API", description="Inteligencia Deportiva", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "ARES 2.0 funcionando"}

@app.get("/predict/{local}/{visitante}")
def predict(local: str, visitante: str):
    # Aquí va la lógica de predicción (la migraremos de tu script original)
    return {"local": local, "visitante": visitante, "prob_local": 65.5}