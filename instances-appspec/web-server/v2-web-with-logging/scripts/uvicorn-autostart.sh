sudo mv uvicorn.service /etc/systemd/system/uvicorn.service

sudo systemctl daemon-reload
sudo systemctl enable uvicorn
sudo systemctl start uvicorn
sudo systemctl status uvicorn
