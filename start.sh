
#!/bin/bash 

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

PROJECT_DIR="$SCRIPT_DIR/mysite"

VENV_DIR="$SCRIPT_DIR/venv"

cd "$PROJECT_DIR" || { echo "not found"; exit 1; }


if [ -f "$VENV_DIR/bin/activate" ]; then
     source "$VENV_DIR/bin/activate"
else
     echo "$SCRIPT_DIR."
     exit 1
fi

LOCAL_IP=$(hostname -I  | awk '{print $1}')

echo "Django server is running at http://$LOCAL_IP:8000"


python3 manage.py runserver 0.0.0.0:8000 





