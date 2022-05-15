from app import create_app, db
from flask_script import Server, Manager
from flask_migrate import Migrate, MigrateCommand
from app.models import BlogPost, User, Comments

app = create_app('production')
manager = Manager(app)
manager.add_command('server', Server)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.shell
def make_shell_context():
    return dict(db=db, bp=BlogPost, user=User, cm=Comments)


@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('test')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
