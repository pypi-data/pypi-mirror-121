import click
import subprocess
import os
import json
import shutil
from pathlib import Path

taint_content = {
    "sources": [
        {
            "name": "UserInput",
            "comment": "Input from the user as parameter"
        }
    ],
    "sinks": [
        {
            "name": "SQLQuery",
            "comment": "SQL query"
        }
    ],
    "rules": [
        {
          "name": "Possible SQL Injection",
          "code": 7001,
          "sources": [ "UserInput" ],
          "sinks": [ "SQLQuery" ],
          "message_format": "UserInput may directly execute the SQL query"
        }
    ]
}

model_content = """
flask.request.args.get: TaintSource[UserInput] = ...
flask.request.form: TaintSource[UserInput] = ...
def sqlite3.Connection.cursor.execute(self, __sql: TaintSink[SQLQuery], __parameters): ...
"""


@click.group()
def protectsql():
    pass


@protectsql.command()
@click.option("--config-path", default=".", show_default=True, type=click.Path())
def init(config_path):
    """
    Initializes the project folder with .pysa and taint.config files
    """
    click.echo("Initializing...")
    os.system("pyre init")
    os.environ["PYRE_TYPESHED"] = str(Path(os.getcwd()) / "typeshed")
    pyre_config = None
    with open('.pyre_configuration', 'r') as fp:
        pyre_config = json.load(fp)
        pyre_config["search_path"] = [os.path.join(Path(os.getcwd()), "typeshed", "stubs")]
        pyre_config["taint_models_path"] = [config_path]
        pyre_config["exclude"] = [".*/site-packages/.*"]
    if os.path.isfile('.pyre_configuration'):
        os.remove('.pyre_configuration')
    with open('.pyre_configuration', "w") as fp:
        fp.write(json.dumps(pyre_config))
    if not os.path.isdir(config_path):
        os.mkdir(config_path)
    model_path = os.path.join(config_path, "models.pysa")
    with open(model_path, 'w') as fp:
        fp.write(model_content)
    click.echo("Created models.pysa file...")
    taint_config_path = os.path.join(config_path, 'taint.config')
    with open(taint_config_path, 'w') as fp:
        content = json.dumps(taint_content, indent=2)
        fp.write(content)
    click.echo("Create taint.config file...")
    click.echo(f"Configuration files generated at '{config_path}'")


@protectsql.command()
def analyze():
		os.system("pyre --noninteractive analyze --no-verify")
