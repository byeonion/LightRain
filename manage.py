#!/usr/bin/env python
import os
from app import create_app, db
from app.models import Article, User, List
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, Article=Article, User=User, List=List)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def deploy():
    """Run deployment tasks."""
    from flask_migrate import upgrade
    from app.models import Article
    
    upgrade()
    
    user_dog = User(name='dog', confirmed=True)
    db.session.add(user_dog)
    db.session.commit()
    
    List.generate()
    Article.generate_fake(30)
    
    
    
if __name__ == '__main__':
    manager.run()
    
    
