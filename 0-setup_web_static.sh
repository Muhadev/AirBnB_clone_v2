#!/bin/bash

# Install Nginx if not already installed
if ! command -v nginx > /dev/null; then
    sudo apt-get -y update
    sudo apt-get -y install nginx
fi

# Create necessary directories
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared

# Create a fake HTML file
sudo echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Set ownership to ubuntu user and group recursively
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
nginx_config="/etc/nginx/sites-available/default"
nginx_alias="location /hbnb_static/ {\n\talias /data/web_static/current/;\n\t}\n"

if ! grep -q "location /hbnb_static/" "$nginx_config"; then
    sudo sed -i "/server_name _;/ a $nginx_alias" "$nginx_config"
fi

# Restart Nginx
sudo service nginx restart
