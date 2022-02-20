# Systemd configure
Sure you has root privage  
First modify "WorkingDirectory" to fsd folder in demo/fsdapi.service  
And copy demo/fsdapi.service to /etc/systemd/system  
And do some shell  
```
systemctl daemon-reload
systemctl enable --now fsdapi
```
Ok!
