sudo systemctl daemon-reload
sudo rm -f /etc/nginx/sites-enabled/default
sudo cp /home/ubuntu/football/nginx/nginx.conf /etc/nginx/sites-available/myapp
sudo ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled/
#sudo ln -s /etc/nginx/sites-available/blog /etc/nginx/sites-enabled
#sudo nginx -t
sudo gpasswd -a ww-data ubuntu
sudo systemctl restart nginx