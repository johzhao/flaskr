import os

from flask_migrate import Migrate
from flask_migrate import MigrateCommand
from flask_script import Manager
from flask_script import Shell

from app import create_app
from app import db
from app.font_ocr.models import FontRecord

config_name = os.environ.get('SERVER_CONFIG', 'default')
app = create_app(config_name)
manager = Manager(app)
migrate = Migrate(app, db)


def make_context():
    return {
        'app': app,
        'db': db,
        'FontRecord': FontRecord,
    }


manager.add_command('shell', Shell(make_context=make_context))

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
