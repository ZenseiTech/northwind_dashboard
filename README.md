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

If you don't want to run a hook at runtime in pre-commit

    SKIP=unittests pre-commit run --all-files

    SKIP=unittests git commit -m <...>

    SKIP=unittests,flake8 git commit -m <...>

Creation of blueprint ...
https://realpython.com/flask-blueprint/

From:

https://icomoon.io/app/#/select

Select icons and Generate Font

Create user from command line. Alway export first:

    export FLASK_APP=northwind.py

    flask shell

    Create user with Administrator role (if the user exist remove first):

        >>> role = Role.query.filter_by(name='Administrator').first()

        >>> u = User(email='barizonte@gmail.com', username='Zensei', role_id=role.id)

        >>> u.password = 'your_secret_password'

        >>> u.role_id = role.id

        >>> db.session.add(u)

        >>> db.session.commit()

    Create user with View role

        >>> role = Role.query.filter_by(name='User').first()

        >>> u = User(email='luis@gmail.com', username='Luis', role_id=role.id)

        >>> u.password = 'secret'

        >>> db.session.add(u)

        >>> db.session.commit()

Load balancer app:

    https://github.com/wg/wrk
