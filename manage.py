from flask_migrate import MigrateCommand
from flask_script import Manager
from app.main import create_app
from app.main.model.load_data import load_db_data
import os


config_name = os.getenv("ENV")
app = create_app(config_name=config_name)
manager = Manager(app)


manager.add_command("db", MigrateCommand)


@manager.command
def add_data():
    load_db_data()



@manager.command
def run():
    app.run(host="127.0.0.1", port=7003,debug=True)


if __name__ == "__main__":
    manager.run()
