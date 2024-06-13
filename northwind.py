"""Northwind application setup."""
import os
import sys

import click
from dotenv import load_dotenv
from flask_migrate import Migrate, upgrade

from app import create_app, db
from app.models import Category, Permission, Role, User

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

COV = None
if os.environ.get("FLASK_COVERAGE"):
    import coverage

    COV = coverage.coverage(branch=True, include="app/*")
    COV.start()


app = create_app(os.getenv("FLASK_CONFIG") or "default")
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    """Allow for access in flask shell the objects."""
    return dict(
        db=db,
        User=User,
        Role=Role,
        Permission=Permission,
        Category=Category,
    )


@app.cli.command()
@click.option(
    "--coverage/--no-coverage", default=False, help="Run tests under code coverage."
)
@click.argument("test_names", nargs=-1)
def test(coverage, test_names):
    """Run the unit tests."""
    if coverage and not os.environ.get("FLASK_COVERAGE"):
        import subprocess

        os.environ["FLASK_COVERAGE"] = "1"
        sys.exit(subprocess.call(sys.argv))

    import unittest

    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        app.logger.info("Coverage Summary:")
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, "tmp/coverage")
        COV.html_report(directory=covdir)
        app.logger.info("HTML version: file://%s/index.html" % covdir)
        COV.erase()


@app.cli.command()
@click.option(
    "--length",
    default=25,
    help="Number of functions to include in the profiler report.",
)
@click.option(
    "--profile-dir", default=None, help="Directory where profiler data files are saved."
)
def profile(length, profile_dir):
    """Start the application under the code profiler."""
    from werkzeug.contrib.profiler import ProfilerMiddleware

    app.wsgi_app = ProfilerMiddleware(
        app.wsgi_app, restrictions=[length], profile_dir=profile_dir
    )
    app.run()


@app.cli.command("load_data")
def data_load():
    """Call the load data to database."""
    from db_backup import load_data

    load_data.load(db, dropall=True)


@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # migrate database to latest revision
    upgrade()

    # create or update user roles
    Role.insert_roles()


def create_secret_token():
    """Create secre token to swarth CRFS."""
    from itsdangerous import URLSafeSerializer

    auth_s = URLSafeSerializer("secret key", "auth")
    return auth_s.dumps({"id": 5, "name": "Secret word"})


if __name__ == "__main__":
    app.run(port=5000, debug=True)
