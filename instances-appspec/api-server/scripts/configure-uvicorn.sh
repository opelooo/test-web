sudo bash -c 'cat <<EOF > /etc/systemd/system/uvicorn.service
[Unit]
Description=Uvicorn FastAPI Server
After=network.target

[Service]
User=root
WorkingDirectory=/home/ec2-user/api-app
ExecStart=/usr/local/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF'

sudo systemctl daemon-reload
sudo systemctl enable uvicorn
sudo systemctl start uvicorn
sudo systemctl status uvicorn
