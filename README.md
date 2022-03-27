# fsd-cert-manager

A simple python script for modify & vaild fsd's cert.txt (different servers)  

# Using with [cfcsim's fsd](https://github.com/cfcsim/fsd)  

Remove `fsdcert.py` and rename `fsdcert.cfcsim.py` to `fsdcert.py`  
(If you want support other version FSD, just send source code use email to me.)

# Manually modify

`num.py` Already

# Use

(FSD server)  
Install requirements package from requirements.txt (`pip install -r requirements.txt`)  
Put the python files to fsd root folder  
Edit `fsdapi.py` and modify token yourself  
And run `gunicorn --log-level=debug --keep-alive=300 -w 4 -b 0.0.0.0:port fsdapi:app`  
the port just tcp port to deploy web server. 1-65535
(A systemd manager plan is ready. See README.systemd.md)  

# Demo usage

See demo/certreg.php (Web server)  
(If you direct use it, DO NOT forget change token and Tencent captcha vaild [or direct delete code about tencent captcha] too!)  
