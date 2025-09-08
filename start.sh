'
#!/usr/bin/env bash
set -e

flask db upgrade || true
exec gunicorn app:app 
