FROM nginx:latest

VOLUME /var/log/nginx/log
## Copy our default nginx config
COPY conf.d/nginx.conf /etc/nginx/nginx.conf
COPY conf.d/ssl/www_gogrocery_ae.crt /etc/nginx/ssl/www_gogrocery_ae.crt
COPY conf.d/ssl/www_gogrocery_ae.csr /etc/nginx/ssl/www_gogrocery_ae.csr
COPY conf.d/ssl/www_gogrocery_ae.key /etc/nginx/ssl/www_gogrocery_ae.key
COPY conf.d/ssl/www_gogrocery_ae.crt /etc/nginx/ssl/www_gogrocery_ae.crt
RUN chmod -R 600 /etc/nginx/ssl/
## Remove default nginx website
RUN rm -rf /usr/share/nginx/html/*
CMD ["nginx", "-g", "daemon off;"]