#!/usr/bin/env bash
set -e

# Necesario para Flask 3
export FLASK_APP=app.py

# Aplica migraciones al arrancar (si no hay historial, lo crea)
flask db upgrade || (flask db stamp head && flask db migrate -m "auto init" && flask db upgrade)

# Arranca la app
exec gunicorn app:app