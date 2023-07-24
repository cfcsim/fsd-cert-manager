# fsd-cert-manager

A simple python script for modify & vaild fsd's cert.txt (different servers)  

# Using with [cfcsim's fsd](https://github.com/cfcsim/fsd)  

Remove `fsdcert.py` and rename `fsdcert.cfcsim.py` to `fsdcert.py`  
(If you want support other version FSD, just send source code to me by email.)

# Command line tool

`python num.py`

# Usage

(FSD server)  
Install requirements from requirements.txt (`pip install -r requirements.txt`)  
Put the python files to fsd root folder.  
Edit `fsdapi.py` and modify token.  
And run `gunicorn --log-level=debug --keep-alive=300 -w 4 -b 0.0.0.0:<port> fsdapi:app`  
(A systemd service is ready. See README.systemd.md)  

# Frontend example

See demo/certreg.php (Web server)  
(If you use it directly, DO NOT forget to change token and Tencent captcha (or delete code about tencent captcha) too!)  
