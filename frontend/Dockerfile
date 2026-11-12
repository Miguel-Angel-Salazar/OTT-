FROM nginx:1.25-alpine

LABEL org.opencontainers.image.title="ott-frontend" \
      org.opencontainers.image.description="Frontend Nginx Reverse Proxy + Static Cache para Plataforma OTT Cinefilo" \
      org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.authors="Equipo OTT - Gestion de la Configuracion"

# Variables de entorno por defecto para el template de Nginx
ENV BACKEND_URL=http://backend:5000
ENV NGINX_ENVSUBST_FILTER="BACKEND_URL"

# Copiar archivos estáticos (CSS, JS, imágenes, videos)
COPY static /usr/share/nginx/html/static

# Copiar plantilla de configuración del Reverse Proxy
COPY nginx.conf.template /etc/nginx/templates/default.conf.template

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD wget -q --spider http://127.0.0.1/auth/login || exit 1

CMD ["nginx", "-g", "daemon off;"]
