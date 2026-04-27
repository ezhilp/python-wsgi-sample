# Setup
python -m venv venv
venv\Scripts\activate

deactivate

# Powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app\main.py

# Run locally
python -m app.main
waitress-serve --listen=0.0.0.0:8080 app.wsgi:app