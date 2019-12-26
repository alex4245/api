from flask_script import Manager
from api.app import create_app
from api.extensions import db

app = create_app('localconfig.Config')
manager = Manager(app)


@manager.command
def create_all():
    db.create_all()


if __name__ == "__main__":
    manager.run()
