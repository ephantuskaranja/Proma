#!/usr/bin/env python
import os
from app import create_app, db, Flask
from flask_script import Manager,Server
from flask_migrate import Migrate, MigrateCommand
from app.models import User, Farmer, Factory, Group, Processor, Produce, CollectionCentre, AppUser, Trip, Collection, Vehicle





app = create_app('development')
manager = Manager(app)
migrate = Migrate(app, db)
server = Server(host="0.0.0.0", port=18083)
manager.add_command("runserver", server)
manager.add_command('db', MigrateCommand)

app.config['SECRET_KEY'] = 'mysecret'







@manager.command
def runtests():
    """ Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def adduser(username, fullname, pin):
    """Register a new user."""
    from getpass import getpass
    password = getpass()
    password2 = getpass(prompt='Confirm: ')
    if password != password2:
        import sys
        sys.exit('Error: passwords do not match.')
    db.create_all()
    user = User(email=username+"@gmail.com", username=username, password=password, name=fullname, user_pin=pin)
    db.session.add(user)
    db.session.commit()
    print('User {0} was registered successfully.'.format(username))


if __name__ == '__main__':
    manager.run()



