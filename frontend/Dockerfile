FROM nginx:alpine

# Variables de entorno por defecto para el template de Nginx
ENV BACKEND_URL=http://backend:5000
ENV NGINX_ENVSUBST_FILTER="BACKEND_URL"

# Copiar archivos estáticos (CSS, JS, imágenes, videos)
COPY static /usr/share/nginx/html/static

# Copiar plantilla de configuración
COPY nginx.conf.template /etc/nginx/templates/default.conf.template

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
