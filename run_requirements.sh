
# run with source run_requirements.sh
# so to export FLASK_APP

pip freeze | xargs pip uninstall -y

pip install -r requirements.txt

export FLASK_APP=northwind.py
