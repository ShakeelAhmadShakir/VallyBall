sudo cp/home/ubuntu/football/gunicorn/gunicorn.socket /etc/systemd/system/gunicorn.
sudo cp /home/ubuntu/football/gunicorn/gunicorn.service /etc/systemd/system/gunicorn.service
sudo systemctl start gunicorn.service
sudo systemctl enable gunicorn.service