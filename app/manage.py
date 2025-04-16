import os
from flask import Flask
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from market import create_app, db

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.command
def create_db():
    """Create the database."""
    db.create_all()

@manager.command
def drop_db():
    """Drop the database."""
    db.drop_all()

if __name__ == '__main__':
    manager.run()
