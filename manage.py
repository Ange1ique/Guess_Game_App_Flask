from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from Guess_Game import app, db

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
