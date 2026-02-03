FROM nginx:alpine

# Copiamos nuestra configuración personalizada
COPY nginx.conf /etc/nginx/nginx.conf

# Copiamos el HTML a la carpeta estática de Nginx
COPY index.html /usr/share/nginx/html/index.html