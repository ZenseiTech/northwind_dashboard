**Build the requirements**:

Create virtual environment

    python3.10 -m venv .venv

    source ./.venv/bin/activate

Read: https://pypi.org/project/pip-tools/

    python -m pip install pip-tools

**Build the requirements**

    pip install -r requirements.txt

**Commit hooks**

    https://pre-commit.com/

    pip install pre-commit

    Run:

        pre-commit install

        Make sure you have created a git branch before running below command and make sure the existance of file:

            .pre-commit-config.yaml

        pre-commit run --all-files


    pre-commit gc: clears unused things
    pre-commit clean: nukes the whole thing


Set PYTHONPATH to see your modules

    export PYTHONPATH="/media/zensei/My Passport/Zensei/Projects/Python/northwind-dashboard/app:$PYTHONPATH"

Make sure that:

    export FLASK_APP=northwind.py

To test:

    flask test

    flask test --coverage



To clean pip

pip freeze | xargs pip uninstall -y


http://localhost:5000/api/v1/categories
