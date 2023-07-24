# Systemd configure
Besure you have root privage.  
First, modify "WorkingDirectory" to fsd folder in demo/fsdapi.service  
And copy demo/fsdapi.service to /etc/systemd/system/  
Then:  
```
systemctl daemon-reload
systemctl enable --now fsdapi
```
Ok!
