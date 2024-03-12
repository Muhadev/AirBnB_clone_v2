#!/usr/bin/env bash
# Sets up a web server for deployment of webstatic content

# Check if Nginx is installed
if ! command -v nginx > /dev/null; then
    sudo apt-get update
    sudo apt-get install -y nginx
fi

mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/
echo "Holberton School" > /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test/ /data/web_static/current

chown -R ubuntu /data/
chgrp -R ubuntu /data/

# Update Nginx configuration
printf %s "server {
    listen 80 default_server;
    listen [::]80 default_server;
    add_header X-Served-By $HOSTNAME;
    root /var/www/html;
    index index.html index.htm;

    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }

    location /redirect_me {
        return 301 https://www.youtube.com/;
    }

    error_page 404 /404.html;
    location /404 {
        root /var/www/html;
        internal;
    }
}" | sudo tee /etc/nginx/sites-available/default > /dev/null

# Check Nginx configuration before restarting
sudo nginx -t && sudo service nginx restart
