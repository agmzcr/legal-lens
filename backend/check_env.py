import os
from dotenv import load_dotenv

# Ruta absoluta al .env
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".env"))
print("Looking for .env in:", dotenv_path)

# Carga explícitamente el .env
load_dotenv(dotenv_path=dotenv_path)

# Imprime valores de prueba
print("ENVIRONMENT =", os.getenv("ENVIRONMENT"))
print("DATABASE_URL =", os.getenv("DATABASE_URL"))
print("OPENROUTER_API_KEY =", os.getenv("OPENROUTER_API_KEY"))
