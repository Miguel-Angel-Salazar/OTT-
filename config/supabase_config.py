import os
from dotenv import load_dotenv
from supabase import create_client

# carga las variables de entorno del .env
load_dotenv()

# credenciales del proyecto de supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# cliente que usan todos los services para hablar con supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
