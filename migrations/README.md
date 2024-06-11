Single-database configuration for Flask.

Make sure that:

export FLASK_APP=northwind.py

$ flask db migrate

$ flask db upgrade

Careful when renaming columns, the created migration script will drop the column and create a new one.
That is not what you want.

flask load_data > db_backup/logs/log.file 2>&1

flask test > db_backup/logs/log.file 2>&1
