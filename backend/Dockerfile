FROM python:3.11-slim

LABEL org.opencontainers.image.title="ott-backend" \
      org.opencontainers.image.description="Backend Flask MVC + Swagger para Plataforma OTT Cinefilo" \
      org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.authors="Equipo OTT - Gestion de la Configuracion"

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=5000

# Dependencias mínimas del sistema para diagnóstico y healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 1. Copiar e instalar dependencias primero para aprovechar caché de capas de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Copiar el código fuente de la aplicación
COPY . .

# 3. Crear y usar usuario no privilegiado (buena práctica de seguridad D3 / D7)
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

# Healthcheck nativo contra el endpoint de salud del API
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:5000/api/health || exit 1

CMD ["python", "app.py"]
