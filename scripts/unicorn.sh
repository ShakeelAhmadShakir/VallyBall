sudo cp/home/ubuntu/Vallyball/gunicorn/gunicorn.socket /etc/systemd/system/gunicorn.
sudo cp /home/ubuntu/Vallyball/gunicorn/gunicorn.service /etc/systemd/system/gunicorn.service
sudo systemctl start gunicorn.service
sudo systemctl enable gunicorn.service